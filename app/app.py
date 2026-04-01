from flask import Flask
import os
from flask import Flask, jsonify

app = Flask(__name__)


DATABASE_URL = "postgresql://ma_db_flask_user:xyRR3jo1vh3sPDa17xxJ9QN2M1u3UnKK@dpg-d76h6olm5p6s73bmopn0-a/ma_db_flask"

@app.route("/")
def home():
    return {"message": "Serveur V12 avec Database connecté !"}

@app.route("/db")
def get_users():
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT * FROM utilisateurs;") # Ta table vue dans Adminer
        rows = cur.fetchall()
        cur.close()
        conn.close()
        return jsonify({"status": "success", "utilisateurs": rows})
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
