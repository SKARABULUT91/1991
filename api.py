import os
import json
import subprocess
import signal
from flask import Flask, jsonify, request
from flask_cors import CORS

app = Flask(__name__)
# CORS ayarını tüm kaynaklara izin verecek şekilde esnettik (Frontend engelini aşmak için)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# --- DOSYA YOLLARI ---
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FILES = {
    "accounts": os.path.join(BASE_DIR, "accounts.json"),
    "settings": os.path.join(BASE_DIR, "settings.json"),
    "reports": os.path.join(BASE_DIR, "gorev_raporu.json"),
    "logs": os.path.join(BASE_DIR, "logs.json"),
    "proxies": os.path.join(BASE_DIR, "proxies.json"),
    "campaigns": os.path.join(BASE_DIR, "campaigns.json"),
    "lock": os.path.join(BASE_DIR, "bot.lock")
}

bot_process = None

# Başlangıçta lock dosyasını temizle (Render restart atarsa bot askıda kalmasın)
if os.path.exists(FILES["lock"]):
    os.remove(FILES["lock"])

# --- YARDIMCI FONKSİYONLAR ---
def read_db(key, default=[]):
    path = FILES.get(key)
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except: return default
    return default

def write_db(key, data):
    with open(FILES.get(key), 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# --- 1. DASHBOARD ANA DAMAR ---
@app.route('/api/bot-report', methods=['GET'])
def get_full_report():
    return jsonify({
        "status": "running" if os.path.exists(FILES["lock"]) else "idle",
        "accounts": read_db("accounts"),
        "campaigns": read_db("campaigns"),
        "proxies": read_db("proxies"),
        "reports": read_db("reports"),
        "logs": read_db("logs"),
        "stats": {
            "is_active": os.path.exists(FILES["lock"]),
            "server_time": os.popen("date +%H:%M:%S").read().strip()
        }
    }), 200

# --- 2. OPERASYON KONTROLLERİ ---
@app.route('/api/start-bot', methods=['POST'])
def start_bot():
    global bot_process
    if os.path.exists(FILES["lock"]):
        return jsonify({"status": "error", "message": "Operasyon zaten sürüyor!"}), 400
    try:
        # Boş dosyaları oluştur ki bot hata vermesin
        for key in ["logs", "reports"]:
            if not os.path.exists(FILES[key]): write_db(key, [])

        with open(FILES["lock"], "w") as f: f.write("running")
        
        # Docker ortamında bazen 'python3' bazen 'python' çalışır.
        # preexec_fn=os.setsid sayesinde stop-bot dediğinde alt işlemleri de öldürürüz.
        bot_process = subprocess.Popen(["python", "bot_engine.py"], preexec_fn=os.setsid)
        
        return jsonify({"status": "success", "message": "Hayalet Ateşlendi!"}), 200
    except Exception as e:
        if os.path.exists(FILES["lock"]): os.remove(FILES["lock"])
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/api/stop-bot', methods=['POST'])
def stop_bot():
    global bot_process
    try:
        if os.path.exists(FILES["lock"]): os.remove(FILES["lock"])
        if bot_process:
            os.killpg(os.getpgid(bot_process.pid), signal.SIGTERM)
            bot_process = None
        return jsonify({"status": "success", "message": "Operasyon durduruldu"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # RENDER İÇİN KRİTİK: Portu ortam değişkeninden al, yoksa 10000 kullan.
    port = int(os.environ.get("PORT", 10000))
    print(f"💎 Kodcum Ajans Backend Motoru Port {port} üzerinden yayında!")
    app.run(debug=False, port=port, host='0.0.0.0')
