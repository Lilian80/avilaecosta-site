from datetime import datetime
from flask import Blueprint, flash, redirect, render_template, request, url_for

from app.database import get_db
from app.data.blocos import BLOCOS
from app.services.scoring import PONTOS_RESPOSTA, calcular_percentual

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return render_template("index.html", blocos=BLOCOS)


@main_bp.route("/diagnostico", methods=["GET", "POST"])
def diagnostico():
    if request.method == "POST":
        db = get_db()
        dados = {campo: request.form.get(campo, "").strip() for campo, _ in BLOCOS[0]["campos"]}
        observacoes_gerais = request.form.get("observacoes_gerais", "").strip()

        respostas_texto = []
        respostas_para_salvar = []

        for bloco in BLOCOS:
            if bloco.get("tipo") in ["dados", "5w2h"]:
                continue
            for idx, pergunta in enumerate(bloco["perguntas"], start=1):
                campo_resposta = f"{bloco['id']}_{idx}"
                campo_obs = f"{bloco['id']}_{idx}_obs"
                resposta = request.form.get(campo_resposta, "Não se aplica")
                observacao = request.form.get(campo_obs, "").strip()
                respostas_texto.append(resposta)
                respostas_para_salvar.append(
                    {
                        "bloco_id": bloco["id"],
                        "bloco_titulo": bloco["titulo"],
                        "pergunta": pergunta,
                        "resposta": resposta,
                        "observacao": observacao,
                        "pontos": PONTOS_RESPOSTA.get(resposta),
                    }
                )

        pontuacao_total, total_avaliavel, percentual, nivel = calcular_percentual(respostas_texto)
        criado_em = datetime.now().strftime("%d/%m/%Y %H:%M")

        cursor = db.execute(
            """
            INSERT INTO diagnosticos (
                criado_em, nome_clinica, responsavel, especialidade, cidade, telefone,
                email, pontuacao_total, total_avaliavel, percentual_conformidade,
                nivel_risco, observacoes_gerais
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                criado_em,
                dados.get("nome_clinica"),
                dados.get("responsavel"),
                dados.get("especialidade"),
                dados.get("cidade"),
                dados.get("telefone"),
                dados.get("email"),
                pontuacao_total,
                total_avaliavel,
                percentual,
                nivel,
                observacoes_gerais,
            ),
        )
        diagnostico_id = cursor.lastrowid

        for item in respostas_para_salvar:
            db.execute(
                """
                INSERT INTO respostas_blocos (
                    diagnostico_id, bloco_id, bloco_titulo, pergunta, resposta, observacao, pontos
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    diagnostico_id,
                    item["bloco_id"],
                    item["bloco_titulo"],
                    item["pergunta"],
                    item["resposta"],
                    item["observacao"],
                    item["pontos"],
                ),
            )

        db.execute(
            """
            INSERT INTO plano_5w2h (
                diagnostico_id, what, why, where_text, who, when_text, how, how_much, status, evidencia
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                diagnostico_id,
                request.form.get("what", "").strip(),
                request.form.get("why", "").strip(),
                request.form.get("where", "").strip(),
                request.form.get("who", "").strip(),
                request.form.get("when", "").strip(),
                request.form.get("how", "").strip(),
                request.form.get("how_much", "").strip(),
                request.form.get("status", "Planejado").strip(),
                request.form.get("evidencia", "").strip(),
            ),
        )
        db.commit()
        flash("Diagnóstico salvo com sucesso.", "success")
        return redirect(url_for("main.resultado", diagnostico_id=diagnostico_id))

    return render_template("diagnostico.html", blocos=BLOCOS)


@main_bp.route("/diagnosticos")
def lista():
    db = get_db()
    diagnosticos = db.execute(
        "SELECT * FROM diagnosticos ORDER BY id DESC"
    ).fetchall()
    return render_template("lista.html", diagnosticos=diagnosticos)


@main_bp.route("/diagnostico/<int:diagnostico_id>")
def resultado(diagnostico_id):
    db = get_db()
    diagnostico = db.execute(
        "SELECT * FROM diagnosticos WHERE id = ?", (diagnostico_id,)
    ).fetchone()
    if diagnostico is None:
        flash("Diagnóstico não encontrado.", "error")
        return redirect(url_for("main.lista"))

    respostas = db.execute(
        "SELECT * FROM respostas_blocos WHERE diagnostico_id = ? ORDER BY id",
        (diagnostico_id,),
    ).fetchall()
    plano = db.execute(
        "SELECT * FROM plano_5w2h WHERE diagnostico_id = ?", (diagnostico_id,)
    ).fetchone()

    return render_template(
        "resultado.html",
        diagnostico=diagnostico,
        respostas=respostas,
        plano=plano,
    )
