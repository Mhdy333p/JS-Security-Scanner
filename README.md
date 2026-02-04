# 🐬 Dolphin 3.0 Large-Scale JS Security Scanner

An elite, local-first **Red Team Security Audit** tool optimized for hardware with limited VRAM (e.g., RTX 3050 Ti 4GB). This tool leverages the `dolphin3:8b` model via Ollama to perform deep security analysis on JavaScript files, even those exceeding standard context windows.

me and gemini

## 🚀 Features

* **VRAM-Aware Chunking:** Automatically splits large `.js` files into manageable chunks to prevent "Out of Memory" errors on 4GB GPUs.
* **Terminal-Inspired UI:** A high-contrast, "Matrix-green" Streamlit interface.
* **Deep Audit Logic:** Configured to identify:
* **Attack Surface:** API endpoints and hardcoded URLs.
* **Injections:** Tracing data into sinks like `eval()` or `innerHTML`.
* **Secrets:** Detection of hardcoded JWTs, API keys, and credentials.
* **Logic Flaws:** Client-side auth bypasses and insecure storage.


* **Streaming Reports:** Watch the AI's thought process in real-time as it audits each section.
* **Report Export:** Download the full aggregated audit as a `.md` file.

## 🛠️ Prerequisites

1. **Ollama installed:** [Download Ollama](https://ollama.ai/)
2. **Dolphin 3 Model:** ```bash
ollama pull dolphin3:8b
```

```


3. **Python Requirements:**
```bash
pip install streamlit ollama

```



## 💻 Installation & Usage

1. **Clone the repository:**
```bash
git clone https://github.com/your-username/dolphin-js-scanner.git
cd dolphin-js-scanner

```


2. **Run the application:**
```bash
streamlit run app.py

```


3. **Perform an Audit:**
* Upload any `.js` file via the drag-and-drop interface.
* Adjust the **Context Window** in the sidebar based on your GPU capability.
* Click **Start Deep Audit** and monitor the "Total Vulnerabilities" metric.



## ⚙️ Configuration

The tool is pre-configured with the following safety and performance guards:

| Setting | Value | Description |
| --- | --- | --- |
| `CHUNK_SIZE` | 15,000 chars | Optimized for ~4k tokens per pass. |
| `TEMPERATURE` | 0.0 | Ensures deterministic, technical, and precise output. |
| `MODEL` | `dolphin3:8b` | Chosen for high reasoning capabilities in coding tasks. |

## ⚠️ Disclaimer

This tool is intended for **authorized security auditing and educational purposes only**. Always ensure you have explicit permission before scanning codebases that you do not own.
