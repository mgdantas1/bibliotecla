from flask import redirect, request, render_template, url_for, Blueprint, flash
from flask_login import logout_user
from sqlalchemy.orm import Session
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models.usuario import Users
from database import engine
perfil_bp = Blueprint('perfil', __name__, template_folder='../templates/perfil')


@perfil_bp.route('/listar_perfil/<int:user_id>', methods=['GET'])
@login_required
def listar_perfil(user_id:int):
    with Session(bind=engine) as db:
        user = db.get(Users, user_id)
    return render_template('perfil/listar.html', user=user)


@perfil_bp.route('/editar_perfil/<int:user_id>', methods=['GET', 'POST'])
@login_required
def editar_perfil(user_id:int):
    with Session(bind=engine) as db:
        user = db.get(Users, user_id)

    if request.method == 'POST':
        nome = request.form.get('nome')
        email = request.form.get('email')

        with Session(bind=engine) as db:
            user = db.get(Users, user_id)
            user.nome = nome
            user.email = email
            db.commit()

        flash('Usuário editado com sucesso!', category='success')
        return redirect(url_for('perfil.listar_perfil', user_id=user_id))

    return render_template('perfil/editar.html', user=user)

@perfil_bp.route('/alterar_senha', methods=['GET', 'POST'])
@login_required
def alterar_senha():
    with Session(bind=engine) as db:
        user = db.get(Users, current_user.id)

        if request.method == 'POST':
            nova_senha = request.form['senha']
            senha_ant = request.form['senha_ant']

            # verificar se a senha antiga está correta
            if not check_password_hash(user.senha, senha_ant):
                flash('Insira a senha correta!', category='error')
                return redirect(url_for('perfil.alterar_senha'))

            # verificar se a senha nova é igual a antiga
            if check_password_hash(user.senha, nova_senha):
                flash('A nova senha deve ser diferente da senha atual.', category='error')
                return redirect(url_for('perfil.alterar_senha'))

            # se a senha digitada for diferente da senha atual e a pessoa digitar a senha correta no campo de senha atual, atualiza a senha
            user.senha = generate_password_hash(nova_senha)
            db.commit()

            flash('Senha modificada com sucesso!', category='success')
            return redirect(url_for('perfil.listar_perfil', user_id=user.id))

    return render_template('alterar_senha.html', user=user)



@perfil_bp.route('/deletar_usuario', methods=['GET'])
@login_required
def deletar_usuario():
    with Session(bind=engine) as db:
        user = db.get(Users, current_user.id)

        for emprestimo in user.emprestimos:
            db.delete(emprestimo)

        logout_user()
        db.delete(user)
        db.commit()

    return redirect(url_for('index'))

