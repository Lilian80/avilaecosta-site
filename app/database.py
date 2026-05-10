import sqlite3
from flask import current_app, g


def get_db():
    if "db" not in g:
        conn = sqlite3.connect(current_app.config["DATABASE"])
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db


def close_db(error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db(app):
    with app.app_context():
        db = get_db()
        db.executescript(
            """
            CREATE TABLE IF NOT EXISTS diagnosticos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                criado_em TEXT NOT NULL,
                nome_clinica TEXT,
                responsavel TEXT,
                especialidade TEXT,
                cidade TEXT,
                telefone TEXT,
                email TEXT,
                pontuacao_total REAL DEFAULT 0,
                total_avaliavel INTEGER DEFAULT 0,
                percentual_conformidade REAL DEFAULT 0,
                nivel_risco TEXT,
                observacoes_gerais TEXT
            );

            CREATE TABLE IF NOT EXISTS respostas_blocos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                diagnostico_id INTEGER NOT NULL,
                bloco_id TEXT NOT NULL,
                bloco_titulo TEXT NOT NULL,
                pergunta TEXT NOT NULL,
                resposta TEXT NOT NULL,
                observacao TEXT,
                pontos REAL DEFAULT 0,
                FOREIGN KEY (diagnostico_id) REFERENCES diagnosticos(id)
            );

            CREATE TABLE IF NOT EXISTS plano_5w2h (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                diagnostico_id INTEGER NOT NULL,
                what TEXT,
                why TEXT,
                where_text TEXT,
                who TEXT,
                when_text TEXT,
                how TEXT,
                how_much TEXT,
                status TEXT,
                evidencia TEXT,
                FOREIGN KEY (diagnostico_id) REFERENCES diagnosticos(id)
            );
            """
        )
        db.commit()
    app.teardown_appcontext(close_db)
