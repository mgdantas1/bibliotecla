from models.livros import Livros
from sqlalchemy.orm import Session
from database import engine
from datetime import date

with Session(bind=engine) as db:
    if db.query(Livros).count() == 0:
        livros = [
            Livros(
                titulo="O Senhor dos Anéis: A Sociedade do Anel",
                autor="J.R.R. Tolkien",
                ano_publicacao=date(1954, 7, 29),
                editora="Allen & Unwin",
                genero="Fantasia",
                resumo="Um grupo parte em uma jornada para destruir um anel poderoso."
            ),
            Livros(
                titulo="1984",
                autor="George Orwell",
                ano_publicacao=date(1949, 6, 8),
                editora="Secker & Warburg",
                genero="Ficção Científica",
                resumo="Um regime totalitário controla todos os aspectos da vida humana."
            ),
            Livros(
                titulo="Dom Casmurro",
                autor="Machado de Assis",
                ano_publicacao=date(1899, 1, 1),
                editora="Tipografia Nacional",
                genero="Romance",
                resumo="Bentinho relembra sua juventude e o amor por Capitu."
            ),
            Livros(
                titulo="Sherlock Holmes: O Cão dos Baskerville",
                autor="Arthur Conan Doyle",
                ano_publicacao=date(1902, 4, 1),
                editora="George Newnes",
                genero="Mistério",
                resumo="Holmes investiga uma lenda que assombra a família Baskerville."
            ),
            Livros(
                titulo="A Menina que Roubava Livros",
                autor="Markus Zusak",
                ano_publicacao=date(2005, 3, 14),
                editora="Picador",
                genero="Drama",
                resumo="A história de uma menina que encontra conforto nos livros durante a guerra."
            ),
        ]

        db.add_all(livros)
        db.commit()
