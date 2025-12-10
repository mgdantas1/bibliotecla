from flask import redirect, request, render_template, url_for, Blueprint, flash
from sqlalchemy.orm import Session
from flask_login import login_user, logout_user, login_required
from models.usuario import Users
from database import engine
from werkzeug.security import check_password_hash, generate_password_hash
auth_bp = Blueprint('auth', __name__, template_folder='../templates/auth')

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        with Session(bind=engine) as session:
            user_exist = session.query(Users).where(Users.email == email).first()
            if not user_exist:
                senha_crip = generate_password_hash(senha)
                user_novo = Users(nome=nome, senha=senha_crip, email=email)
                session.add(user_novo)
                session.commit()
                login_user(user_novo)
                flash('Usuário cadastrado com sucesso!', category='susess')
                return redirect(url_for('index'))
            flash('Usuário já cadastrado!', category='error')
    return render_template('cadastro.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        with Session(bind=engine) as session:
            user_exist = session.query(Users).where(Users.email == email).first()
            if user_exist and check_password_hash(user_exist.senha, senha):
                login_user(user_exist)
                return redirect(url_for('index'))
            flash('Dados incorretos!', category='error')
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))