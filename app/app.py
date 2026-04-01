from flask import Flask
import os
from flask import Flask, jsonify

app = Flask(__name__)


DATABASE_URL = os.environ.get("DATABASE_URL")

@app.route("/db")
def get_db_users():
    try:
        # Connexion à PostgreSQL
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        
        # Requête pour lire la table que tu as créée
        cur.execute("SELECT * FROM utilisateurs;")
        users = cur.fetchall()
        
        cur.close()
        conn.close()
        
        return jsonify({"status": "success", "data": users})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)})
        
@app.route("/")
def home():
    return "Flask + Docker + GHCR + Terraform + Render"

@app.route("/health")
def health():
    return {"status": "Tout est ok ou pas"}

@app.route("/info")
def info():
    return {
        "app": "Flask Render",
        "student": "Veloso Alexis",
        "version": "v1"
    }

@app.route("/env")
def env():
    return {"env": os.getenv("ENV")}

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
