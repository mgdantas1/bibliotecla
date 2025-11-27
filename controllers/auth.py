from flask import redirect, request, render_template, url_for, Blueprint, flash
from sqlalchemy.orm import Session
from datetime import date, timedelta
from flask_login import login_user
from models.usuario import Users
from werkzeug.security import check_password_hash, generate_password_hash
auth_bp = Blueprint('auth', __name__, template_folder='../templates')

@auth_bp.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        senha = request.form['senha']
        with Session(bind=engine) as db:
            user_exist = db.query(Users).where(Users.email == email).first()
            if not user_exist:
                user_novo = Users(nome=nome, senha=senha, email=email)
                login_user(user_novo)
                return redirect(url_for('index'))
            flash('Usuário já cadastrado!')
    return render_template('cadastro.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        with Session(bind=engine) as db:
            user_exist = db.query(Users).where(Users.email == email).first()
            if user_exist and check_password_hash(user_exist.senha, senha):
                login_user(user_exist)
                return redirect(url_for('index'))
            flash('Dados inválidas!')
    return render_template('login.html')

