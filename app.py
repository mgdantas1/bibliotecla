from database import popular_livros
from flask import Flask, render_template
from flask_login import LoginManager
from sqlalchemy.orm import Session
from database import engine
from models.usuario import Users
from controllers.auth import auth_bp

app = Flask(__name__)
app.secret_key = 'Segredo'

login_manager = LoginManager()
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):
    with Session(bind=engine) as session:
        usuario = session.query(Users).where(Users.id == user_id).first()
    return usuario

@app.route('/')
def index():
    return render_template('index.html')

app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
