import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

DATABASE_URL = "postgresql://ma_db_flask_user:xyRR3jo1vh3sPDa17xxJ9QN2M1u3UnKK@dpg-d76h6olm5p6s73bmopn0-a/ma_db_flask"

@app.route("/")
def home():
    return """
    <html>
        <head>
            <title>Mon Projet Cloud</title>
            <style>
                body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #eef2f7; text-align: center; padding-top: 100px; }
                .card { background: white; padding: 40px; border-radius: 15px; box-shadow: 0 10px 25px rgba(0,0,0,0.1); display: inline-block; }
                h1 { color: #2c3e50; }
                .btn { background: #3498db; color: white; padding: 12px 25px; text-decoration: none; border-radius: 5px; font-weight: bold; }
                .btn:hover { background: #2980b9; }
            </style>
        </head>
        <body>
            <div class="card">
                <h1>🚀 Bienvenue sur mon Site Cloud</h1>
                <p>Projet réalisé par <strong>Veloso Alexis</strong></p>
                <p>Technologies : Flask + Docker + Terraform + Render</p>
                <br>
                <a href="/db" class="btn">Voir la Base de Données</a>
            </div>
        </body>
    </html>
    """

@app.route("/db")
def get_db_visual():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT * FROM utilisateurs;")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        # Construction du tableau HTML
        html = """
        <html>
        <head>
            <title>Dashboard Utilisateurs</title>
            <style>
                body { font-family: sans-serif; background-color: #f8f9fa; padding: 30px; }
                .container { max-width: 800px; margin: auto; background: white; padding: 20px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
                h2 { color: #007bff; border-bottom: 2px solid #007bff; padding-bottom: 10px; }
                table { width: 100%; border-collapse: collapse; margin-top: 20px; }
                th, td { padding: 15px; text-align: left; border-bottom: 1px solid #eee; }
                th { background-color: #007bff; color: white; }
                tr:hover { background-color: #f8f9fa; }
                .back-link { margin-top: 20px; display: block; text-decoration: none; color: #666; }
            </style>
        </head>
        <body>
            <div class="container">
                <h2>👥 Liste des Utilisateurs en Base</h2>
                <table>
                    <tr><th>ID</th><th>Nom / Prénom</th></tr>
        """
        for row in rows:
            html += f"<tr><td>{row[0]}</td><td>{row[1]}</td></tr>"
        
        html += """
                </table>
                <a href="/" class="back-link">← Retour à l'accueil</a>
            </div>
        </body>
        </html>
        """
        return html
    except Exception as e:
        return f"<h3>Erreur de connexion :</h3><p>{str(e)}</p>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
