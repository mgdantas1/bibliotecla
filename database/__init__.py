from models import Base
from sqlalchemy import create_engine
from models.emprestimos import Emprestimos
from models.usuario import Users

engine = create_engine('mysql+mysqlconnector://root@localhost:3306/db_bibliotecla')
Base.metadata.create_all(bind=engine)