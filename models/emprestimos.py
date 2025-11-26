from sqlalchemy import ForeignKey, Date
from sqlalchemy.orm import Mapped, mapped_column
from datetime import date
from models import Base

class Emprestimos(Base):
    __tablename__ = 'emprestimos'
    id:Mapped[int] = mapped_column(primary_key=True, autoincrement=True, nullable=False)
    data_emprestimo:Mapped[str] = mapped_column(nullable=False)
    data_prazo:Mapped[date] = mapped_column(Date, nullable=False)
    data_devolucao:Mapped[date] = mapped_column(Date, nullable=False)

    user_id:Mapped[int] = mapped_column(ForeignKey('users.id'))
    livro_id:Mapped[int] = mapped_column(ForeignKey('livros.id'))