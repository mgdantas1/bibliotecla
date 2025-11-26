from flask import redirect, request, render_template, url_for, Blueprint, flash
from datetime import date, timedelta

emprestimo_bp = Blueprint('emprestimos', __name__, template_folder='../templates')

@emprestimo_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data_atual = date.today()
        data_prazo = data_atual + timedelta(days=30)
    return redirect(url_for('emprestimos.visualizar'))

