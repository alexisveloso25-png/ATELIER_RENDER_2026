import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

# URL de ta base de données Render
DATABASE_URL = "postgresql://ma_db_flask_user:xyRR3jo1vh3sPDa17xxJ9QN2M1u3UnKK@dpg-d76h6olm5p6s73bmopn0-a/ma_db_flask"

STYLE = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --bg: #080c14;
        --surface: rgba(255,255,255,0.035);
        --surface-hover: rgba(255,255,255,0.065);
        --border: rgba(255,255,255,0.08);
        --border-glow: rgba(99,210,255,0.3);
        --accent: #63d2ff;
        --accent2: #a78bfa;
        --text: #e2eaf4;
        --muted: #5a6a82;
        --success: #34d399;
        --success-bg: rgba(52,211,153,0.1);
        --glow: 0 0 40px rgba(99,210,255,0.12);
    }

    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    body {
        font-family: 'Syne', sans-serif;
        background-color: var(--bg);
        color: var(--text);
        min-height: 100vh;
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 60px 20px 80px;
        position: relative;
        overflow-x: hidden;
    }

    /* Ambient background blobs */
    body::before {
        content: '';
        position: fixed;
        top: -200px; left: -200px;
        width: 700px; height: 700px;
        background: radial-gradient(circle, rgba(99,210,255,0.06) 0%, transparent 70%);
        pointer-events: none;
        z-index: 0;
    }
    body::after {
        content: '';
        position: fixed;
        bottom: -150px; right: -150px;
        width: 600px; height: 600px;
        background: radial-gradient(circle, rgba(167,139,250,0.06) 0%, transparent 70%);
        pointer-events: none;
        z-index: 0;
    }

    .container {
        width: 100%;
        max-width: 860px;
        position: relative;
        z-index: 1;
    }

    /* ─── TOPBAR ─── */
    .topbar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 14px 24px;
        margin-bottom: 36px;
        backdrop-filter: blur(12px);
    }
    .topbar-brand {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: var(--accent);
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }
    .topbar-status {
        display: flex;
        align-items: center;
        gap: 8px;
        font-size: 0.78rem;
        color: var(--success);
        font-family: 'JetBrains Mono', monospace;
    }
    .pulse {
        width: 8px; height: 8px;
        background: var(--success);
        border-radius: 50%;
        box-shadow: 0 0 0 0 rgba(52,211,153,0.5);
        animation: pulse 1.8s infinite;
    }
    @keyframes pulse {
        0%   { box-shadow: 0 0 0 0 rgba(52,211,153,0.5); }
        70%  { box-shadow: 0 0 0 8px rgba(52,211,153,0); }
        100% { box-shadow: 0 0 0 0 rgba(52,211,153,0); }
    }

    /* ─── HERO ─── */
    .hero {
        text-align: center;
        padding: 60px 40px;
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 20px;
        margin-bottom: 24px;
        backdrop-filter: blur(12px);
        position: relative;
        overflow: hidden;
    }
    .hero::before {
        content: '';
        position: absolute;
        top: -1px; left: 50%; transform: translateX(-50%);
        width: 60%; height: 1px;
        background: linear-gradient(90deg, transparent, var(--accent), transparent);
    }
    .hero-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--accent);
        letter-spacing: 0.18em;
        text-transform: uppercase;
        margin-bottom: 20px;
        opacity: 0.9;
    }
    .hero h1 {
        font-size: 2.8rem;
        font-weight: 800;
        line-height: 1.1;
        background: linear-gradient(135deg, #e2eaf4 30%, var(--accent) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        margin-bottom: 16px;
    }
    .hero-sub {
        color: var(--muted);
        font-size: 1rem;
        line-height: 1.6;
    }
    .hero-sub strong { color: var(--accent2); font-weight: 600; }

    /* ─── CARDS GRID ─── */
    .cards {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        margin-bottom: 24px;
    }
    .card {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 24px 26px;
        backdrop-filter: blur(12px);
        transition: border-color 0.2s, background 0.2s;
    }
    .card:hover { border-color: var(--border-glow); background: var(--surface-hover); }
    .card-label {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.68rem;
        color: var(--muted);
        letter-spacing: 0.14em;
        text-transform: uppercase;
        margin-bottom: 10px;
    }
    .card-value {
        font-size: 1.1rem;
        font-weight: 700;
        color: var(--text);
    }

    /* ─── BUTTON ─── */
    .btn {
        display: inline-flex;
        align-items: center;
        gap: 10px;
        background: linear-gradient(135deg, var(--accent), #4ab8e8);
        color: #060a10;
        padding: 14px 32px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: 700;
        font-size: 0.95rem;
        letter-spacing: 0.02em;
        transition: all 0.25s;
        box-shadow: 0 0 24px rgba(99,210,255,0.18);
    }
    .btn:hover {
        transform: translateY(-3px);
        box-shadow: 0 0 40px rgba(99,210,255,0.35);
    }
    .btn-wrap { text-align: center; margin-top: 10px; }

    /* ─── BACK LINK ─── */
    .back {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        color: var(--accent);
        text-decoration: none;
        font-size: 0.88rem;
        font-family: 'JetBrains Mono', monospace;
        opacity: 0.8;
        transition: opacity 0.2s;
        margin-bottom: 28px;
    }
    .back:hover { opacity: 1; }

    /* ─── SECTION HEADER ─── */
    .section-head {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    .section-head h2 {
        font-size: 1.5rem;
        font-weight: 700;
    }
    .count-badge {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        background: rgba(99,210,255,0.12);
        color: var(--accent);
        border: 1px solid rgba(99,210,255,0.2);
        padding: 4px 12px;
        border-radius: 99px;
    }

    /* ─── TABLE ─── */
    .table-wrap {
        background: var(--surface);
        border: 1px solid var(--border);
        border-radius: 16px;
        overflow: hidden;
        backdrop-filter: blur(12px);
    }
    table { width: 100%; border-collapse: collapse; }
    thead { background: rgba(99,210,255,0.06); border-bottom: 1px solid var(--border); }
    th {
        text-align: left;
        padding: 14px 22px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.7rem;
        letter-spacing: 0.15em;
        text-transform: uppercase;
        color: var(--muted);
    }
    td {
        padding: 16px 22px;
        border-bottom: 1px solid rgba(255,255,255,0.04);
        font-size: 0.95rem;
    }
    tbody tr:last-child td { border-bottom: none; }
    tbody tr { transition: background 0.15s; }
    tbody tr:hover { background: var(--surface-hover); }

    .id-chip {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.8rem;
        color: var(--accent2);
        background: rgba(167,139,250,0.1);
        border: 1px solid rgba(167,139,250,0.15);
        padding: 3px 10px;
        border-radius: 6px;
    }
    .status-badge {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        background: var(--success-bg);
        color: var(--success);
        border: 1px solid rgba(52,211,153,0.2);
        padding: 4px 12px;
        border-radius: 99px;
        font-size: 0.76rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }
    .status-badge::before {
        content: '';
        width: 6px; height: 6px;
        background: var(--success);
        border-radius: 50%;
    }

    /* ─── DB INFO ─── */
    .db-info {
        margin-top: 16px;
        padding: 14px 22px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--muted);
        border-top: 1px solid var(--border);
        display: flex;
        align-items: center;
        gap: 8px;
    }

    /* ─── FOOTER ─── */
    .footer {
        margin-top: 48px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        color: var(--muted);
        text-align: center;
        letter-spacing: 0.08em;
    }

    /* ─── FADE IN ─── */
    @keyframes fadeUp {
        from { opacity: 0; transform: translateY(18px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    .topbar  { animation: fadeUp 0.4s ease both; }
    .hero    { animation: fadeUp 0.5s 0.05s ease both; }
    .cards   { animation: fadeUp 0.5s 0.1s ease both; }
    .btn-wrap{ animation: fadeUp 0.5s 0.15s ease both; }
    .back    { animation: fadeUp 0.4s ease both; }
    .section-head { animation: fadeUp 0.45s 0.05s ease both; }
    .table-wrap   { animation: fadeUp 0.5s 0.1s ease both; }

    /* ─── ERROR ─── */
    .error-box {
        background: rgba(239,68,68,0.08);
        border: 1px solid rgba(239,68,68,0.2);
        border-radius: 14px;
        padding: 32px;
        text-align: center;
    }
    .error-box h2 { color: #f87171; margin-bottom: 12px; }
    .error-box p { font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: var(--muted); }
</style>
"""

@app.route("/")
def home():
    return f"""
    <html>
        <head>
            <title>Veloso Alexis | Cloud App</title>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            {STYLE}
        </head>
        <body>
            <div class="container">

                <div class="topbar">
                    <span class="topbar-brand">// cloud_app v12.0</span>
                    <div class="topbar-status">
                        <div class="pulse"></div>
                        SERVICE OPÉRATIONNEL
                    </div>
                </div>

                <div class="hero">
                    <p class="hero-label">// application déployée</p>
                    <h1>Bienvenue sur<br>mon App Cloud</h1>
                    <p class="hero-sub">
                        Déployée avec <strong>Docker</strong>, <strong>Terraform</strong> &amp; <strong>Render</strong>
                    </p>
                </div>

                <div class="cards">
                    <div class="card">
                        <div class="card-label">Étudiant</div>
                        <div class="card-value">Veloso Alexis</div>
                    </div>
                    <div class="card">
                        <div class="card-label">Statut</div>
                        <div class="card-value" style="color: var(--success);">En ligne ✅</div>
                    </div>
                    <div class="card">
                        <div class="card-label">Version</div>
                        <div class="card-value" style="font-family: 'JetBrains Mono', monospace; font-size:0.95rem; color: var(--accent);">12.0 — 2026</div>
                    </div>
                    <div class="card">
                        <div class="card-label">Base de données</div>
                        <div class="card-value" style="font-family: 'JetBrains Mono', monospace; font-size:0.85rem; color: var(--accent2);">PostgreSQL</div>
                    </div>
                </div>

                <div class="btn-wrap">
                    <a href="/db" class="btn">
                        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>
                        Accéder aux données SQL
                    </a>
                </div>

            </div>
            <div class="footer">// veloso_alexis · docker · terraform · render · 2026</div>
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

        count = len(rows)
        rows_html = ""
        for row in rows:
            rows_html += f"""
            <tr>
                <td><span class="id-chip">#{row[0]:03d}</span></td>
                <td>{row[1]}</td>
                <td><span class="status-badge">Actif</span></td>
            </tr>"""

        return f"""
        <html>
            <head>
                <title>Dashboard | Utilisateurs</title>
                <meta charset="UTF-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                {STYLE}
            </head>
            <body>
                <div class="container">

                    <div class="topbar">
                        <span class="topbar-brand">// cloud_app v12.0</span>
                        <div class="topbar-status">
                            <div class="pulse"></div>
                            SERVICE OPÉRATIONNEL
                        </div>
                    </div>

                    <a href="/" class="back">← retour accueil</a>

                    <div class="section-head">
                        <h2>👥 Gestion des Utilisateurs</h2>
                        <span class="count-badge">{count} enregistrement{'s' if count != 1 else ''}</span>
                    </div>

                    <div class="table-wrap">
                        <table>
                            <thead>
                                <tr>
                                    <th>ID</th>
                                    <th>Nom / Prénom</th>
                                    <th>Statut</th>
                                </tr>
                            </thead>
                            <tbody>
                                {rows_html}
                            </tbody>
                        </table>
                        <div class="db-info">
                            <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M21 12c0 1.66-4 3-9 3s-9-1.34-9-3"/><path d="M3 5v14c0 1.66 4 3 9 3s9-1.34 9-3V5"/></svg>
                            Connecté à : dpg-d76h6olm5p6s73bmopn0-a · PostgreSQL
                        </div>
                    </div>

                </div>
                <div class="footer">// veloso_alexis · docker · terraform · render · 2026</div>
            </body>
        </html>
        """
    except Exception as e:
        return f"""
        <html>
            <head><title>Erreur</title><meta charset="UTF-8">{STYLE}</head>
            <body>
                <div class="container">
                    <div class="topbar">
                        <span class="topbar-brand">// cloud_app v12.0</span>
                    </div>
                    <a href="/" class="back">← retour accueil</a>
                    <div class="error-box">
                        <h2>❌ Erreur de connexion</h2>
                        <p>{str(e)}</p>
                    </div>
                </div>
            </body>
        </html>
        """

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
