from flask import redirect, request, render_template, url_for, Blueprint, flash
from datetime import date, timedelta
from database import engine
from sqlalchemy.orm import Session
from models.emprestimos import Emprestimos
from models.livros import Livros
from flask_login import login_required, current_user

emprestimo_bp = Blueprint('emprestimo', __name__, template_folder='../templates/emprestimos')

@emprestimo_bp.route('/visualizar_emprestimos', methods=['GET'])
@login_required
def visualizar_emprestimos():
    with Session(bind=engine) as db:
        emprestimos = db.query(Emprestimos).where(Emprestimos.user_id == current_user.id).all()
    return render_template('emprestimos/visualizar.html', emprestimos=emprestimos)


@emprestimo_bp.route('/register_emprestimo/<int:livro_id>')
@login_required
def register_emprestimo(livro_id: int):
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

    flash('Empréstimo realizado com sucesso!')
    return redirect(url_for('emprestimo.visualizar_emprestimos'))
    

@emprestimo_bp.route('/editar_emprestimo/<int:emprestimo_id>', methods=['GET', 'POST'])
@login_required
def editar_emprestimo(emprestimo_id: int):
    with Session(bind=engine) as db:
        emprestimo = db.get(Emprestimos, emprestimo_id)

    if request.method == 'POST':
        data_emprestimo = request.form['data_emprestimo']
        data_prazo = request.form['data_prazo']
        data_devolucao = request.form['data_devolucao']
        with Session(bind=engine) as db:
            emprestimo = db.get(Emprestimos, emprestimo_id)
            emprestimo.data_emprestimo = data_emprestimo
            emprestimo.data_prazo = data_prazo
            emprestimo.data_devolucao = data_devolucao
            db.commit()
        
        flash('Empréstimo editado com sucesso!')
        return redirect(url_for('emprestimo.visualizar_emprestimos'))
    
    return render_template('emprestimos/editar.html', emprestimo=emprestimo)

# falta criar a rota de deletar emprestimo
    


