from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Criar tabela no banco se não existir
def init_db():
    conn = sqlite3.connect("estoque.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            quantidade INTEGER NOT NULL
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    conn = sqlite3.connect("estoque.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos")
    produtos = cursor.fetchall()
    conn.close()
    return render_template("index.html", produtos=produtos)

@app.route("/adicionar", methods=["POST"])
def adicionar():
    nome = request.form.get("nome")
    quantidade = request.form.get("quantidade")
    if nome and quantidade:
        conn = sqlite3.connect("estoque.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO produtos (nome, quantidade) VALUES (?, ?)", (nome, quantidade))
        conn.commit()
        conn.close()
    return redirect("/")

@app.route("/remover/<int:id>")
def remover(id):
    conn = sqlite3.connect("estoque.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM produtos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    conn = sqlite3.connect("estoque.db")
    cursor = conn.cursor()

    if request.method == "POST":
        nome = request.form.get("nome")
        quantidade = request.form.get("quantidade")
        cursor.execute("UPDATE produtos SET nome = ?, quantidade = ? WHERE id = ?", (nome, quantidade, id))
        conn.commit()
        conn.close()
        return redirect("/")

    cursor.execute("SELECT * FROM produtos WHERE id = ?", (id,))
    produto = cursor.fetchone()
    conn.close()
    return render_template("edit.html", produto=produto)

if __name__ == "__main__":
    app.run(debug=True)
