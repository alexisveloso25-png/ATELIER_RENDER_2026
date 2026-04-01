import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

# URL de ta base de données Render
DATABASE_URL = "postgresql://ma_db_flask_user:xyRR3jo1vh3sPDa17xxJ9QN2M1u3UnKK@dpg-d76h6olm5p6s73bmopn0-a/ma_db_flask"

# Design CSS moderne
STYLE = """
<style>
    :root {
        --primary: #4f46e5;
        --primary-hover: #4338ca;
        --bg: #f8fafc;
        --card-bg: #ffffff;
        --text-main: #1e293b;
        --text-muted: #64748b;
    }
    body { 
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; 
        background-color: var(--bg); 
        color: var(--text-main);
        margin: 0;
        display: flex;
        flex-direction: column;
        align-items: center;
        min-height: 100vh;
        padding: 40px 20px;
    }
    .container {
        width: 100%;
        max-width: 900px;
        background: var(--card-bg);
        padding: 40px;
        border-radius: 16px;
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    h1 { color: var(--primary); margin-bottom: 10px; text-align: center; font-size: 2rem; }
    .subtitle { text-align: center; color: var(--text-muted); margin-bottom: 30px; font-size: 1.1rem; }
    
    table { width: 100%; border-collapse: collapse; margin-top: 20px; border-radius: 8px; overflow: hidden; }
    thead { background-color: var(--primary); color: white; }
    th { text-align: left; padding: 15px; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.05em; }
    td { padding: 15px; border-bottom: 1px solid #e2e8f0; font-size: 1rem; }
    tr:last-child td { border-bottom: none; }
    tr:hover { background-color: #f1f5f9; }

    .status-badge {
        background: #dcfce7;
        color: #166534;
        padding: 4px 12px;
        border-radius: 99px;
        font-size: 0.8rem;
        font-weight: 600;
    }

    .btn {
        display: inline-block;
        background-color: var(--primary);
        color: white;
        padding: 12px 24px;
        border-radius: 8px;
        text-decoration: none;
        font-weight: 600;
        margin-top: 20px;
        transition: 0.3s;
    }
    .btn:hover { background-color: var(--primary-hover); transform: translateY(-2px); }
    .footer { margin-top: 40px; color: var(--text-muted); font-size: 0.9rem; }
</style>
"""

@app.route("/")
def home():
    return f"""
    <html>
        <head><title>Projet Alexis | Accueil</title>{STYLE}</head>
        <body>
            <div class="container" style="text-align: center;">
                <h1>🚀 Bienvenue sur mon Application Cloud</h1>
                <p class="subtitle">Déployée avec <strong>Docker, Terraform & Render</strong></p>
                <div style="background: #f1f5f9; padding: 20px; border-radius: 12px; margin-bottom: 30px;">
                    <p>Étudiant : <strong>Veloso Alexis</strong></p>
                    <p>Statut du service : <span class="status-badge">En ligne ✅</span></p>
                </div>
                <a href="/db" class="btn">Accéder aux données SQL</a>
            </div>
            <div class="footer">Version 12.0 - 2026</div>
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

        rows_html = ""
        for row in rows:
            rows_html += f"<tr><td><strong>#{row[0]}</strong></td><td>{row[1]}</td><td><span class='status-badge'>Utilisateur Actif</span></td></tr>"

        return f"""
        <html>
            <head><title>Base de Données | Dashboard</title>{STYLE}</head>
            <body>
                <div class="container">
                    <a href="/" style="text-decoration: none; color: var(--primary); font-weight: bold;">← Accueil</a>
                    <h1 style="margin-top:20px;">👥 Gestion des Utilisateurs</h1>
                    <p class="subtitle">Données récupérées en direct depuis PostgreSQL</p>
                    <table>
                        <thead>
                            <tr><th>ID</th><th>Nom / Prénom</th><th>Statut</th></tr>
                        </thead>
                        <tbody>
                            {rows_html}
                        </tbody>
                    </table>
                </div>
                <div class="footer">Connecté à : dpg-d76h6olm5p6s73bmopn0-a</div>
            </body>
        </html>
        """
    except Exception as e:
        return f"<div class='container'><h1>❌ Erreur</h1><p>{str(e)}</p><a href='/'>Retour</a></div>"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
