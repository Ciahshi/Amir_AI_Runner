## نوشته شده توسط امير سياوشي
## Telegram id: @Ciahshi

from flask import Flask, render_template, request, jsonify, Response
from model_loader import ModelRunner
import json
import time
import psutil
import socket

app = Flask(__name__)
runner = ModelRunner()

def is_port_open(port):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", port))
            return False
        except:
            return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/scan')
def scan_models():
    models = runner.scan_models()
    return jsonify({"models": models})

@app.route('/api/start', methods=['POST'])
def start_model():
    data = request.json
    model_path = data.get('path')
    model_type = data.get('type', 'gguf')
    port = int(data.get('port', 8000))
    n_ctx = int(data.get('n_ctx', 4096))
    n_threads = int(data.get('n_threads', psutil.cpu_count(logical=True) // 2))

    if not model_path:
        return jsonify({"success": False, "message": "مسیر مدل انتخاب نشده!"})

    if is_port_open(port):
        return jsonify({"success": False, "message": f"پورت {port} اشغال است! لطفاً پورت دیگری انتخاب کنید."})

    success, msg = runner.start_server(model_path, model_type, port, n_ctx, n_threads)
    return jsonify({"success": success, "message": msg})

@app.route('/api/stop', methods=['POST'])
def stop_model():
    success, msg = runner.stop_server()
    return jsonify({"success": success, "message": msg})

@app.route('/api/status')
def status():
    status = runner.get_status()
    port_free = not is_port_open(8000)  # if open means free, so not free means running? Actually check properly.
    # بهتره وضعیت رو از خود پروسه بگیریم
    return jsonify(status)

@app.route('/api/logs')
def logs():
    log_lines = runner.read_logs(100)
    return jsonify({"logs": log_lines})

@app.route('/api/system')
def system_stats():
    return jsonify({
        "cpu": psutil.cpu_percent(),
        "ram": psutil.virtual_memory().percent,
        "ram_used": f"{psutil.virtual_memory().used / (1024**3):.1f} GB",
        "ram_total": f"{psutil.virtual_memory().total / (1024**3):.1f} GB"
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """پروکسی برای چت با مدل (فرض می‌کنیم سرور روی ۸۰۰۰ هست)"""
    data = request.json
    prompt = data.get('prompt', '')
    port = data.get('port', 8000)
    if not prompt:
        return jsonify({"error": "پرامپت خالی است"}), 400

    try:
        import requests
        # بررسی OpenAI compatibility (llama-cpp-python)
        url = f"http://127.0.0.1:{port}/v1/completions"
        payload = {
            "prompt": prompt,
            "max_tokens": 256,
            "temperature": 0.7,
            "stream": False
        }
        response = requests.post(url, json=payload, timeout=60)
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            # تلاش با فرمت /chat/completions
            url_chat = f"http://127.0.0.1:{port}/v1/chat/completions"
            payload_chat = {
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 256,
                "temperature": 0.7
            }
            response = requests.post(url_chat, json=payload_chat, timeout=60)
            return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": f"خطا در ارتباط با مدل: {str(e)}"}), 500

if __name__ == '__main__':
    print("""
    ╔═══════════════════════════════════════════╗
    ║   🚀 Amir AI Runner - Control Panel      ║
    ║   Running on: http://127.0.0.1:5000      ║
    ║   Base URL for Models: http://127.0.0.1:8000/v1
    ╚═══════════════════════════════════════════╝
    """)
    app.run(debug=False, host='0.0.0.0', port=5000, threaded=True)
