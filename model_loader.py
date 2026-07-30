## نوشته شده توسط امير سياوشي
## Telegram id: @Ciahshi

import os
import sys
import subprocess
import platform
import psutil
import glob
import json

class ModelRunner:
    def __init__(self):
        self.process = None
        self.model_type = None

    def scan_models(self, directory="./models"):
        """اسکن پوشه برای پیدا کردن مدل‌های GGUF و پوشه‌های Transformers"""
        models = []
        if not os.path.exists(directory):
            os.makedirs(directory, exist_ok=True)
            return models

        # 1. اسکن فایل‌های GGUF
        for gguf_file in glob.glob(os.path.join(directory, "*.gguf")):
            size_mb = os.path.getsize(gguf_file) / (1024 * 1024)
            models.append({
                "name": os.path.basename(gguf_file),
                "path": gguf_file,
                "type": "gguf",
                "size": f"{size_mb:.1f} MB",
                "quant": self._guess_quant(gguf_file)
            })

        # 2. اسکن پوشه‌های Transformers (دارای config.json)
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            if os.path.isdir(item_path) and os.path.exists(os.path.join(item_path, "config.json")):
                try:
                    with open(os.path.join(item_path, "config.json"), "r") as f:
                        config = json.load(f)
                        model_type = config.get("model_type", "transformers")
                except:
                    model_type = "transformers"
                models.append({
                    "name": item,
                    "path": item_path,
                    "type": model_type,
                    "size": "N/A",
                    "quant": "FP16/BF16"
                })
        return models

    def _guess_quant(self, path):
        """تشخیص کوانتیزاسیون از اسم فایل (Q4_K_M, Q5, etc)"""
        name = os.path.basename(path).upper()
        if "Q4_K_M" in name: return "Q4_K_M"
        if "Q5_K_M" in name: return "Q5_K_M"
        if "Q8_0" in name: return "Q8_0"
        if "F16" in name: return "F16"
        return "GGUF"

    def start_server(self, model_path, model_type, port=8000, n_ctx=4096, n_threads=None):
        """اجرای مدل روی پورت مشخص"""
        if self.process and self.process.poll() is None:
            return False, "یک سرور در حال اجراست!"

        if n_threads is None:
            n_threads = psutil.cpu_count(logical=True) // 2

        cmd = None
        if model_type == "gguf":
            # استفاده از سرور رسمی llama-cpp-python
            cmd = [
                sys.executable, "-m", "llama_cpp.server",
                "--model", model_path,
                "--port", str(port),
                "--n_ctx", str(n_ctx),
                "--n_threads", str(n_threads)
            ]
        elif model_type in ["transformers", "llama", "mistral", "gpt2"]:
            # بارگذاری با Transformers + FastAPI (یک سرور موقت)
            cmd = [
                sys.executable, "-c", f"""
import uvicorn
from fastapi import FastAPI, Request
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

app = FastAPI()
model = AutoModelForCausalLM.from_pretrained("{model_path}", device_map="auto", torch_dtype=torch.float16)
tokenizer = AutoTokenizer.from_pretrained("{model_path}")

@app.post("/v1/completions")
async def completions(request: Request):
    data = await request.json()
    prompt = data.get("prompt", "")
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    outputs = model.generate(**inputs, max_new_tokens=256)
    text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return {{"choices": [{{"text": text}}]}}

uvicorn.run(app, host="0.0.0.0", port={port})
"""
            ]
        else:
            return False, f"نوع مدل {model_type} پشتیبانی نمی‌شود."

        try:
            # ایجاد لاگ فایل
            log_dir = "./logs"
            os.makedirs(log_dir, exist_ok=True)
            log_file = open(os.path.join(log_dir, "server.log"), "a", encoding="utf-8")

            self.process = subprocess.Popen(
                cmd,
                stdout=log_file,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
            )
            self.model_type = model_type
            return True, f"سرور با موفقیت روی پورت {port} شروع به کار کرد (PID: {self.process.pid})"
        except Exception as e:
            return False, f"خطا در اجرا: {str(e)}"

    def stop_server(self):
        """خاموش کردن کامل سرور"""
        if not self.process:
            return False, "هیچ سروری در حال اجرا نیست!"

        try:
            # کشتن پروسه اصلی و فرزندان
            parent = psutil.Process(self.process.pid)
            children = parent.children(recursive=True)
            for child in children:
                child.terminate()
            parent.terminate()

            # صبر برای پایان
            gone, alive = psutil.wait_procs(children + [parent], timeout=3)
            for p in alive:
                p.kill()

            self.process = None
            return True, "سرور با موفقیت متوقف شد."
        except Exception as e:
            return False, f"خطا در توقف: {str(e)}"

    def get_status(self):
        if self.process and self.process.poll() is None:
            return {
                "running": True,
                "pid": self.process.pid,
                "type": self.model_type
            }
        return {"running": False}

    def read_logs(self, lines=50):
        """خواندن آخرین لاگ‌ها"""
        log_path = "./logs/server.log"
        if not os.path.exists(log_path):
            return ["لاگی موجود نیست."]
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                all_lines = f.readlines()
                return all_lines[-lines:]
        except:
            return ["خطا در خواندن لاگ."]
