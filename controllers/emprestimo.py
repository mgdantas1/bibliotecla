from flask import redirect, request, render_template, url_for, Blueprint, flash
from datetime import date, timedelta
from database import engine
from sqlalchemy.orm import Session
from models.emprestimos import Emprestimos
from flask_login import login_required, current_user

emprestimo_bp = Blueprint('emprestimo', __name__, template_folder='../templates')

@emprestimo_bp.route('/visualizar', methods=['GET'])
@login_required
def visualizar():
    return render_template('emprestimo/emprestimos.html')


@emprestimo_bp.route('/register', methods=['POST'])
@login_required
def register():
    user_id = current_user.id
    data_atual = date.today()
    data_prazo = data_atual + timedelta(days=30)
    with Session(bind=engine) as db:
        novo_emprestimo = Emprestimos(data_atual=data_atual, data_prazo=data_prazo, user_id=user_id)
        db.add(novo_emprestimo)
        db.commit()
    
    flash('Empréstimo realizado com sucesso!')
    return redirect(url_for('emprestimo.visualizar'))
    

@emprestimo_bp.route('/editar/<int:emprestimo_id>', methods=['GET', 'POST'])
@login_required
def editar(emprestimo_id: int):
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
        return redirect(url_for('emprestimo.visualizar'))
    
    return render_template('emprestimo/editar.html')

# falta criar a rota de deletar emprestimo
    


