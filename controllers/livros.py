from flask import Blueprint, render_template
from flask_login import login_required
from sqlalchemy.orm import Session
from database import engine
from models.livros import Livros

livros_bp = Blueprint('livro', __name__, template_folder='../templates/livros')

@livros_bp.route('/listar_livros')
@login_required
def listar_livros():
    with Session(bind=engine) as db:
        livros = db.query(Livros).all()
    return render_template('livros/listar.html', livros=livros)

