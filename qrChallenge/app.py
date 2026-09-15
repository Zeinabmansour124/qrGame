from flask import Flask, render_template, request, jsonify
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <h1>Bienvenue</h1>
    <p>QR1 : /qr1</p>
    <p>QR2 : /qr2</p>
    <p>Réponse : /reponse</p>
    """

def get_db_connection():
    import sqlite3
    conn = sqlite3.connect("database.db")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/qr1", methods=["GET", "POST"])
def qr1():
    if request.method == "GET":
        return render_template("qr1.html")

    # POST : accepte JSON (fetch) ou formulaire classique
    if request.is_json:
        numero = str(request.get_json().get("numero", "")).strip()
    else:
        numero = request.form.get("numero", "").strip()

    conn = get_db_connection()

    solution = conn.execute("SELECT * FROM solutions WHERE numero = ?", (numero,)).fetchone()
    if solution is None:
        conn.close()
        return jsonify({"success": False, "message": "Numéro inconnu."}), 404

    usage = conn.execute("SELECT * FROM usage WHERE numero = ?", (numero,)).fetchone()
    if usage is None:
        conn.close()
        return jsonify({"success": False, "message": "Aucune entrée usage pour ce numéro."}), 500
    if usage["qr1_utilise"] == 1:
        conn.close()
        return jsonify({"success": False, "message": "Cet indice a déjà été récupéré."}), 403

    conn.execute("UPDATE usage SET qr1_utilise = 1 WHERE numero = ?", (numero,))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "indice": solution["indice1"]})


@app.route("/qr2", methods=["POST", "GET"])
def qr2():
    if request.method == "GET":
        return render_template("qr2.html")

    # POST : accepte JSON (fetch) ou formulaire classique
    if request.is_json:
        numero = str(request.get_json().get("numero", "")).strip()
    else:
        numero = request.form.get("numero", "").strip()

    conn = get_db_connection()

    solution = conn.execute("SELECT * FROM solutions WHERE numero = ?", (numero,)).fetchone()
    if solution is None:
        conn.close()
        return jsonify({"success": False, "message": "Numéro inconnu."}), 404

    usage = conn.execute("SELECT * FROM usage WHERE numero = ?", (numero,)).fetchone()
    if usage is None:
        conn.close()
        return jsonify({"success": False, "message": "Aucune entrée usage pour ce numéro."}), 500
    if usage["qr1_utilise"] == 0:
        conn.close()
        return jsonify({"success": False, "message": "Vous devez d'abord scanner le premier QR code."}), 403
    if usage["qr2_utilise"] == 1:
        conn.close()
        return jsonify({"success": False, "message": "Cet indice a déjà été récupéré."}), 403

    conn.execute("UPDATE usage SET qr2_utilise = 1 WHERE numero = ?", (numero,))
    conn.commit()
    conn.close()

    return jsonify({"success": True, "indice": solution["indice2"]})


@app.route("/response", methods=["POST", "GET"])
def reponse():
    if request.method == "GET":
        return render_template("response.html")

    # POST : accepte les données en JSON (fetch) ou en formulaire classique
    if request.is_json:
        data = request.get_json()
        numero = str(data.get("numero", "")).strip()
        reponse_donnee = str(data.get("reponse", "")).strip()
    else:
        numero = request.form.get("numero", "").strip()
        reponse_donnee = request.form.get("reponse", "").strip()

    if not numero or not reponse_donnee:
        return jsonify({"success": False, "message": "Numéro et réponse requis."}), 400

    conn = get_db_connection()

    solution = conn.execute(
        "SELECT * FROM solutions WHERE numero = ?", (numero,)
    ).fetchone()

    if solution is None:
        conn.close()
        return jsonify({"success": False, "message": "Numéro inconnu."}), 404

    usage = conn.execute(
        "SELECT * FROM usage WHERE numero = ?", (numero,)
    ).fetchone()

    if usage is None:
        conn.close()
        return jsonify({"success": False, "message": "Aucune entrée usage pour ce numéro."}), 500

    if usage["qr2_utilise"] == 0:
        conn.close()
        return jsonify({"success": False, "message": "Vous devez d'abord scanner le second QR code."}), 403

    if usage["validee"] == 1:
        conn.close()
        return jsonify({"success": False, "message": "Ce numéro a déjà validé une réponse."}), 403

    if reponse_donnee.lower() != solution["reponse"].strip().lower():
        conn.close()
        return jsonify({"success": False, "message": "Réponse incorrecte."}), 200

    conn.execute(
        "UPDATE usage SET validee = 1, horodatage_validation = ? WHERE numero = ?",
        (datetime.now().isoformat(), numero)
    )
    conn.commit()
    conn.close()

    return jsonify({"success": True, "message": "Bravo ! Montrez cet écran au stand."})


if __name__ == "__main__":
    app.run(debug=True)