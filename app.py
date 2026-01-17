from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import date

app = Flask(__name__)

def get_db():
    return sqlite3.connect("database.db")

@app.route("/", methods=["GET", "POST"])
def vendas():
    if request.method == "POST":
        data = request.form["data"]
        tipo = request.form["tipo"]
        forma = request.form["forma"]
        valor = request.form["valor"]

        db = get_db()
        db.execute(
            "INSERT INTO vendas (data, tipo_venda, forma_pagamento, valor) VALUES (?, ?, ?, ?)",
            (data, tipo, forma, valor)
        )
        db.commit()
        db.close()

        return redirect("/")

    return render_template("vendas.html")

@app.route("/resumo")
def resumo():
    db = get_db()

    diario = db.execute("""
        SELECT forma_pagamento, SUM(valor)
        FROM vendas
        WHERE data = ?
        GROUP BY forma_pagamento
    """, (date.today(),)).fetchall()

    mensal = db.execute("""
        SELECT forma_pagamento, SUM(valor)
        FROM vendas
        WHERE strftime('%Y-%m', data) = strftime('%Y-%m', 'now')
        GROUP BY forma_pagamento
    """).fetchall()

    db.close()

    return render_template("resumo.html", diario=diario, mensal=mensal)

app.run(debug=True)
