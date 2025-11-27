from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models import Base

class Users(Base):
    __tablename__ = 'users'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    nome:Mapped[str] = mapped_column(String(100), nullable=False)
    email:Mapped[str] = mapped_column(String(100), nullable=False)
    senha:Mapped[str] = mapped_column(String(230), nullable=False)

    emprestimos = relationship('Emprestimos', backref='user')