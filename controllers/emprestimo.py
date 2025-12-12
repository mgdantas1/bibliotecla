from flask import redirect, request, render_template, url_for, Blueprint, flash
from datetime import date, timedelta
from database import engine
from sqlalchemy.orm import Session
from models.emprestimos import Emprestimos
from models.livros import Livros
from flask_login import login_required, current_user

emprestimo_bp = Blueprint('emprestimo', __name__, template_folder='../templates/emprestimos')

def definir_status(data_prazo: date, data_devolucao: date | None) -> str:
    data_atual = date.today()

    if data_devolucao:
        return "Devolvido"

    if data_atual > data_prazo:
        return "Atrasado"

    return "Pendente"


@emprestimo_bp.route('/listar_emprestimos', methods=['GET'])
@login_required
def listar_emprestimos():
    with Session(bind=engine) as db:
        emprestimos = db.query(Emprestimos).where(Emprestimos.user_id == current_user.id).all()

        # atualizar status
        for emprestimo in emprestimos:
            novo_status = definir_status(emprestimo.data_prazo, emprestimo.data_devolucao)
            if novo_status != emprestimo.status:
                emprestimo.status = novo_status

        db.commit()

        return render_template('emprestimos/listar.html', emprestimos = emprestimos)


@emprestimo_bp.route('/register_emprestimo/<int:livro_id>')
@login_required
def register_emprestimo(livro_id: int):
    with Session(bind=engine) as db:

        verificar_livro = db.query(Livros).filter_by(id = livro_id).first()
    
    if verificar_livro and verificar_livro.quantidade > 0:
        user_id = current_user.id
        data_atual = date.today()
        data_prazo = data_atual + timedelta(days=30)
        with Session(bind=engine) as db:
            novo_emprestimo = Emprestimos(data_emprestimo=data_atual, data_prazo=data_prazo, user_id=user_id, livro_id=livro_id)
            db.add(novo_emprestimo)
            db.commit()
        
        with Session(bind=engine) as db:
            livro = db.get(Livros, livro_id)
            livro.quantidade -= 1
            db.commit()
        
        flash('Empréstimo realizado com sucesso!', category='success')
        return redirect(url_for('emprestimo.listar_emprestimos'))
    
    flash('O empréstimo não pode ser realizado!', category='error')
    return redirect(url_for('livro.listar_livros'))

    

@emprestimo_bp.route('/editar_emprestimo/<int:emprestimo_id>', methods=['GET', 'POST'])
@login_required
def editar_emprestimo(emprestimo_id: int):
    with Session(bind=engine) as db:
        emprestimo = db.get(Emprestimos, emprestimo_id)
        if emprestimo:
            if request.method == 'POST':
                data_emprestimo = request.form['data_emprestimo']
                data_prazo = request.form['data_prazo']
                data_devolucao = request.form['data_devolucao']
                status = request.form['status']
                with Session(bind=engine) as db:
                    if emprestimo.status == 'Devolvido':
                        flash("A ação não pode ser realizada!", category='error')
                        return redirect(url_for('emprestimo.listar_emprestimos'))
                    emprestimo = db.get(Emprestimos, emprestimo_id)
                    emprestimo.data_emprestimo = data_emprestimo
                    emprestimo.data_prazo = data_prazo
                    emprestimo.data_devolucao = data_devolucao
                    emprestimo.status = status
                    db.commit()
                
                flash('Empréstimo editado com sucesso!', category='success')
                return redirect(url_for('emprestimo.listar_emprestimos'))
            return render_template('emprestimos/editar.html', emprestimo=emprestimo)
        flash("Emprestimo não encontrado", category='error')
        return redirect(url_for("emprestimo.listar_emprestimos"))


@emprestimo_bp.route('/devolver_livro/<int:emprestimo_id>', methods=['GET', 'POST'])
@login_required
def devolver_livro(emprestimo_id):
    with Session(bind=engine) as db:
        emprestimo = db.get(Emprestimos, emprestimo_id)

        if not emprestimo:
            flash("Emprestimo não encontrado", category='error')
            return redirect(url_for("emprestimo.visualizar_emprestimo"))

        if emprestimo.user_id != current_user.id:
            flash("Você não tem permissão para devolver esse livro", category='error')
            return redirect(url_for("emprestimo.visualizar_emprestimo"))

        if emprestimo.status == "Devolvido":
            flash("Este livro já foi devolvido", category='error')
            return redirect(url_for("emprestimo.visualizar_emprestimo"))
    
        emprestimo.status = "Devolvido"
        emprestimo.data_devolucao = date.today()
        emprestimo.livro.quantidade += 1

        db.commit()

    flash('O livro foi devolvido', category='success')
    return redirect(url_for("emprestimo.listar_emprestimos"))


@emprestimo_bp.route('/deletar_emprestimo/<int:emprestimo_id>', methods=['GET', 'POST'])
@login_required
def deletar_emprestimo(emprestimo_id):
    with Session(bind=engine) as db:
        emprestimo = db.get(Emprestimos, emprestimo_id)
        if emprestimo and emprestimo.status == 'Devolvido':
            db.delete(emprestimo)
            db.commit()
            flash("Emprestimo deletado com sucesso", category='success')
            return redirect(url_for('emprestimo.listar_emprestimos'))
        
        flash("A ação não pode ser realizada!", category='error')
        return redirect(url_for('emprestimo.listar_emprestimos'))

