from sqlalchemy import String, Date
from sqlalchemy.orm import Mapped, mapped_column
from models import Base
from datetime import date

class Livros(Base):
    __tablename__ = 'livros'

    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    titulo:Mapped[str] = mapped_column(String(150), nullable=False)
    autor:Mapped[str] = mapped_column(String(150), nullable=False)
    ano_publicacao:Mapped[date] = mapped_column(Date, nullable=False)
    editora:Mapped[str] = mapped_column(String(50), nullable=False)
    genero:Mapped[str] = mapped_column(String(50), nullable=False)
    resumo:Mapped[str] = mapped_column(String(200), nullable=False)
    quantidade:Mapped[int] = mapped_column(nullable=False)

