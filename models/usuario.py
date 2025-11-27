from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models import Base
from flask_login import UserMixin

class Users(Base, UserMixin):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    nome:Mapped[str] = mapped_column(String(100), nullable=False)
    email:Mapped[str] = mapped_column(String(100), nullable=False)
    senha:Mapped[str] = mapped_column(String(260), nullable=False)

    emprestimos = relationship('Emprestimos', backref='user')

    def get_id(self):
        return str(self.id)
