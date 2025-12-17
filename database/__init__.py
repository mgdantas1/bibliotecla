from models import Base
from sqlalchemy import create_engine
from models.emprestimos import Emprestimos
from models.usuario import Users

engine = create_engine('sqlite:///database/bibliotecla.db')
Base.metadata.create_all(bind=engine)