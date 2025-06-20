# ⚡ Langflow CLI Runner

> Your personal **Langflow launcher**, right from the terminal. Automate workflows, inject dynamic tweaks, upload files to flows, and talk to your Langflow apps like a boss. No UI required. Just code.

---

## ✨ What is This?

A powerful CLI tool that lets you **interact with your Langflow apps programmatically** using the Langflow API. Perfect for scripting, testing, automation, or integrating flows into larger systems.

---

## 🔧 Features at a Glance

✅ Run Langflow flows via command-line
📦 Upload files to specific components in the flow
🧠 Customize flow behavior with runtime tweaks
📃 Save formatted or raw responses
📢 Optional verbose mode for debugging
🌍 Pulls secrets from `.env` or pass them live

---

## 🧪 Quick Start

### 1️⃣ Install dependencies

```bash
pip install requests python-dotenv
```

Add `langflow` if you want file upload support:

```bash
pip install langflow
```

---

### 2️⃣ Setup your `.env`

```env
LANGFLOW_ID=your_langflow_id
FLOW_ID=your_flow_id
APPLICATION_TOKEN=your_langflow_api_token
```

---

### 3️⃣ Run a Flow

```bash
python langflow_runner.py "Hello, Langflow!"
```

Or pass everything manually:

```bash
python langflow_runner.py "Hi!" \
  --endpoint your_flow_id \
  --application_token sk-abc123xyz
```

---

## 🚀 Advanced Examples

### Upload a file and parse it:

```bash
python langflow_runner.py "Analyze this file" \
  --upload_file ./data.csv \
  --components ParseData-r4Fhk \
  --application_token sk-abc123xyz
```

---

### Add some 🔥 tweaks:

```bash
python langflow_runner.py "Let's chat" \
  --tweaks '{"GroqModel-ZMgtx": {"temperature": 0.9}}' \
  --application_token sk-abc123xyz
```

---

## 🧰 All CLI Options

| Argument              | Description                                      |
| --------------------- | ------------------------------------------------ |
| `message`             | Your message/input prompt                        |
| `--endpoint`          | Flow ID (or set via `.env`)                      |
| `--application_token` | Langflow API token                               |
| `--upload_file`       | Path to file to upload                           |
| `--components`        | Comma-separated component IDs for file injection |
| `--tweaks`            | Tweaks in JSON format                            |
| `--output_type`       | e.g. `chat`, `text`, etc.                        |
| `--input_type`        | e.g. `chat`, `text`, etc.                        |
| `--save_output`       | File path to save the JSON response              |
| `--verbose`           | Print debug logs                                 |
| `--raw`               | Output raw JSON instead of pretty print          |

---

## 💾 Save Output

```bash
python langflow_runner.py "Save this!" \
  --save_output response.json
```

---

## 💬 Example Tweaks JSON

```json
{
  "GroqModel-ZMgtx": {
    "temperature": 0.75,
    "top_p": 0.9
  }
}
```

Use it with:

```bash
--tweaks '{"GroqModel-ZMgtx": {"temperature": 0.75, "top_p": 0.9}}'
```

---

## 🧠 Why Use This?

Whether you're a hacker automating workflows, a dev building pipelines, or just tired of clicking around the Langflow UI, this tool gives you total **programmatic power** over your Langflow projects.

---

## 🛠 Built With

* 🐍 Python 3.10+
* 🌐 [Langflow API](https://github.com/logspace-ai/langflow)
* ⚙️ argparse, dotenv, requests

---

## ❤️ Pro Tip

Add an alias to your shell:

```bash
alias runflow="python langflow_runner.py"
```

Now you can do:

```bash
runflow "Summarize this document..."
```

---
