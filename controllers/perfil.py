from flask import redirect, request, render_template, url_for, Blueprint, flash
from flask_login import logout_user
from sqlalchemy.orm import Session
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
from models.usuario import Users
from database import engine
perfil_bp = Blueprint('perfil', __name__, template_folder='../templates/perfil')


@perfil_bp.route('/visulaizar_perfil/<int:user_id>', methods=['GET'])
@login_required
def visualizar_perfil(user_id:int):
    with Session(bind=engine) as db:
        user = db.get(Users, user_id)
    return render_template('perfil.html', user=user)


@perfil_bp.route('/editar_perfil/<int:user_id>', methods=['GET', 'POST'])
@login_required
def editar_perfil(user_id:int):
    with Session(bind=engine) as db:
        user = db.get(Users, user_id)

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')
        senha = request.form.get('senha')

        with Session(bind=engine) as db:
            user = db.get(Users, user_id)
            user.nome = nome
            user.email = email
            user.senha = generate_password_hash(senha)
            db.commit()

        flash('Usuário editado com sucesso!')
        return redirect(url_for('perfil.visualizar_perfil', user_id=user_id))

    return render_template('perfil/editar.html', user=user)


@perfil_bp.route('/deletar_usuario')
@login_required
def deletar_usuario():
    with Session(bind=engine) as db:
        user = db.get(Users, current_user.id)

        for emprestimo in user.emprestimos:
            db.delete(emprestimo)

        logout_user()
        db.delete(user)
        db.commit()

    flash("Usuário deletado com sucesso!")
    return redirect(url_for('index'))

