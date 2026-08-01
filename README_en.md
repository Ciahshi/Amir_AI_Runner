# 🚀 Amir AI Runner

**Easy Setup and Management of Offline Large Language Models (LLMs) on Your Local Machine**

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey)]()

Amir AI Runner is a powerful and completely free tool that allows you to run large language models (such as LLaMA, Gemma, Mistral, etc.) completely offline on your computer. By providing a beautiful web interface and an OpenAI-compatible API, this application makes the process of running heavy models as simple as possible.

---

## 📸 Preview

| Main Dashboard | Quick Chat | System Monitoring |
| :---: | :---: | :---: |
| ![Dashboard](https://amirgpt.ir/3.png) | ![Chat](https://amirgpt.ir/2.png) | ![Monitor](https://amirgpt.ir/1.png) |

---

## ✨ Key Features

- ✅ **Multi-Format Support**: Run GGUF models (`.gguf` files) and Transformers (HuggingFace folders).
- 🎨 **Professional Web Interface**: A beautiful dashboard with Dark Mode for managing models.
- 🔌 **OpenAI-Compatible API**: Once running, you can use any tool that works with the OpenAI API.
- 💬 **Built-in Chatbox**: Quick model testing without the need for separate software.
- 📊 **Real-time Monitoring**: Live display of CPU and RAM usage.
- 🎮 **Process Management**: Easy server start and stop with a single click.
- 📝 **Log Viewer**: View server output for troubleshooting.
- 🔧 **Extensible**: The code structure is designed to easily add support for new frameworks.
- 🌐 **Remote Access**: Ability to connect from other devices on the local network.

---

## 📋 System Requirements

| Hardware Component | Minimum Requirement | Recommended for Smooth Experience |
| :--- | :--- | :--- |
| **Processor (CPU)** | 4-Core (Intel Core i5 / AMD Ryzen 5) | 8-Core or more (Intel Core i7 / AMD Ryzen 7) |
| **Memory (RAM)** | 8 GB | 16 GB or more (for 7B+ parameter models) |
| **Graphics Card (GPU)** | Optional (Runs on CPU) | NVIDIA with at least 6 GB VRAM for CUDA acceleration |
| **Storage** | 10 GB free space | 50+ GB (to store multiple models) |
| **Operating System** | Windows 10/11, Linux (Ubuntu 20.04+), macOS 12+ | - |

---

## 🛠️ Software Prerequisites

| Software | Version | Description |
| :--- | :--- | :--- |
| **Python** | 3.8 to 3.11 | Versions 3.12 and above may cause compatibility issues. |
| **pip** | Latest version | For installing required libraries. |
| **Git** (Optional) | Latest version | For cloning the project repository. |

---

## 📦 Step-by-Step Installation Guide

### 1. Get the Project Code

```bash
# Via Git (Recommended)
git clone https://github.com/Ciahshi/Amir_AI_Runner
cd Amir_AI_Runner

# Or manually: Download the project files and extract them.
```

### 2. Create a Virtual Environment (Recommended)
To avoid conflicts with other Python projects, create a virtual environment:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Required Libraries:

```bash
pip install -r requirements.txt
```

---

## 📂 Preparing Models
Create a folder named `models` in the root of the project (if it doesn't exist). Place your models in this folder using one of the two methods below:

| Model Type | How to place in the `models` folder | Example |
| :--- | :--- | :--- |
| **GGUF** (`.gguf` file) | Copy the `.gguf` file directly. | `models/llama-2-7b.Q4_K_M.gguf` |
| **Transformers** (HuggingFace folder) | Copy the folder containing `config.json` and model weight files. | `models/gemma-2b/` (including config.json, pytorch_model.bin, etc.) |

> **Note:** You can download GGUF models from the HuggingFace website or other reliable sources.

---

## 🔌 Connecting to the Model via Base URL
After starting the server, the model is accessible via `http://127.0.0.1:{port}/v1`. This server is fully compatible with the OpenAI API, so you can use various tools to communicate with it.

### Example using `curl` in Terminal
```bash
curl http://127.0.0.1:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello, how are you?", "max_tokens": 50}'
```

### Example using `requests` library in Python
```python
import requests

response = requests.post(
    "http://127.0.0.1:8000/v1/completions",
    json={"prompt": "What is the meaning of life?", "max_tokens": 100}
)

if response.status_code == 200:
    print(response.json()["choices"][0]["text"])
else:
    print("Error:", response.text)
```

### Connecting from other devices on the network
If you want to connect to the server from another device on the network:
1. In the `app.py` file, ensure `host='0.0.0.0'`.
2. Find your device's IP address (using `ipconfig` on Windows or `ifconfig` on Linux).
3. Use the address `http://{IP-ADDRESS}:8000/v1`.

---

## 🗂️ Project Structure
```text
amir-ai-runner/
├── app.py                 # Core application (Flask + Process Control)
├── model_loader.py        # Model loading and management logic
├── requirements.txt       # List of required libraries
├── templates/
│   └── index.html         # User Dashboard (Frontend)
├── models/                # Models folder (place your models here)
│   ├── your_model.gguf
│   └── your_hf_model/     # Transformers models folder
├── logs/                  # Server logs (created automatically)
│   └── server.log
└── README.md              # This file
```

---

## 🛠️ Troubleshooting Common Errors

| Error | Cause | Solution |
| :--- | :--- | :--- |
| `ConnectionRefusedError: [WinError 10061]` | The model server did not start on the specified port. | 1. Ensure `llama-cpp-python[server]` is installed correctly.<br>2. Change the port to another number (e.g., `8001`).<br>3. Check the logs for the exact error. |
| `ModuleNotFoundError: No module named 'llama_cpp'` | The required library is not installed. | Reinstall the library: `pip install llama-cpp-python[server] --force-reinstall` |
| `Address already in use` | The desired port is occupied by another application. | Change the port to another number or close the occupying application. |
| `OutOfMemoryError` (for Transformers models) | System RAM is insufficient to load the model. | 1. Decrease the Context Length (e.g., to 1024 or 2048).<br>2. Use a smaller model (e.g., a 3B parameter version instead of 7B). |
| **Model is not shown in the list** | The model is not in the `models/` folder or its format is not supported. | Ensure the `.gguf` file or the folder containing `config.json` is located in the `models/` path. |
| **Logs are empty or not updating** | The log file is not created or there is no access to it. | Create a `logs/` folder in the project root and ensure the application has write access to it. |
| **Dashboard page does not open** | Port 5000 is occupied or Flask is not running. | Change the Flask port in `app.py` or close the previous process. |

---

## ⚙️ Advanced Tips for Pro Users

### Changing Processing Threads
By default, the application uses half of the logical CPU cores. To change this value, modify the `n_threads` value when calling `start_server` in the `app.py` file.

### Storing Logs
All server outputs are saved in the `logs/server.log` file. You can open this file for a closer inspection of errors.

### Remote Connection (Local Network)
If you want to connect to the server from another device on the network, ensure `host='0.0.0.0'` in the `app.py` file. Then use your device's IP address instead of `127.0.0.1`.

### Adding Support for a New Framework
To add support for other frameworks (like ExLlamaV2, MLC, or GPTQ-for-LLaMA), simply extend the `start_server` method in the `model_loader.py` file and add a new condition for the desired model type.

### Default Transformers Model Settings
If needed, you can change the `device_map` and `torch_dtype` parameters in the Transformers section in `model_loader.py` to load the model on the GPU or with a different precision.

---

## 📞 Contact Me
- 📧 **Email:** amirsiavoshi629@gmail.com
- 🐙 **GitHub:** [github.com/Ciahshi](https://github.com/Ciahshi)
- ✈️ **Telegram:** [@Ciahshi](https://t.me/Ciahshi)

---

## 📝 Conclusion
With **Amir AI Runner**, running offline models on your personal system becomes as simple as possible. This tool is highly powerful and flexible, and by providing a standard API, it enables connectivity to various applications and tools. For developers, researchers, and AI enthusiasts seeking privacy and complete control over their models, this is an excellent choice.

> **Made with ❤️ for the Iranian AI community**  
> **Version:** 1.0.0 | **Release Date:** 2026/07/31

---

## 📑 Citation / ارجاع

If you use Amir AI Runner in your research or projects, please cite it as follows:
اگر از این پروژه در تحقیقات یا پروژه‌های خود استفاده می‌کنید، لطفاً به صورت زیر ارجاع دهید:

**English (BibTeX):**
```bibtex
@software{Siavoshi_Amir_AI_Runner_2026,
  author = {Siavoshi, Amirali},
  title = {Amir AI Runner: Easy Setup and Management of Offline LLMs},
  year = {2026},
  url = {https://github.com/Ciahshi/Amir_AI_Runner},
  version = {1.0.0}
}
```

**Persian (فارسی):**
```text
سیاوشی، امیرعلی. (۱۴۰۵). Amir AI Runner: راه‌اندازی و مدیریت آسان مدل‌های آفلاین زبان بزرگ (نسخه ۱.۰.۰) [نرم‌افزار رایانه‌ای]. قابل دسترسی در: https://github.com/Ciahshi/Amir_AI_Runner
```
