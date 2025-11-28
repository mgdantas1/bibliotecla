from flask import redirect, request, render_template, url_for, Blueprint, flash
from flask_login import logout_user
from sqlalchemy.orm import Session
from flask_login import login_user, login_required, current_user
from models.usuario import Users
from database import engine
from werkzeug.security import check_password_hash, generate_password_hash
perfil_bp = Blueprint('perfil', __name__, template_folder='../templates/perfil')

@perfil_bp.route('/editar_perfil/<int:user_id>', methods=['GET', 'POST'])
@login_required
def editar_perfil(user_id:int):
    with Session(bind=engine) as db:
        user = db.get(Users, user_id)

    if request.method == 'POST':
        user_nome = request.form.get('user_nome')
        user_email = request.form.get('user_email')
        user_senha = request.form.get('user_senha')

        with Session(bind=engine) as db:
            user_bd = db.get(Users, user_id)
            user_bd.user_nome = user_nome
            user_bd.user_email = user_email
            user_bd.user_senha = user_senha
            db.commit()

        flash('Usuário editado com sucesso!')
        return redirect(url_for('perfil.editar_perfil', user_id=user_id))

    return render_template('perfil/editar.html', user=user)

@perfil_bp.route('/deletar_usuario')
@login_required
def deletar_usuario():
    with Session(bind=engine) as db:
        user = db.get(Users, current_user.id)
        logout_user()
        db.delete(user)
        db.commit()

    flash("Usuário deletado com sucesso!")
    return redirect(url_for('index'))

