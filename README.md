# 🛡️ OpenSourceGuardian

A security scanner for GitHub repositories — paste any repo URL, get a full vulnerability report on its dependencies, and ask questions about it using AI.

Built with **Python**, **Streamlit**, **OSV API**, and **Groq LLM**.

---

## What it does

- Clones any public GitHub repository
- Detects the language (Python / JavaScript)
- Finds dependency files (`requirements.txt`, `pyproject.toml`, `package.json`)
- Queries the [OSV.dev](https://osv.dev) database for known CVEs
- Lets you chat with an AI about the security report

---

## Demo

> Enter a GitHub URL → Click Scan → Ask questions like:
> - *"Is this repo safe to use?"*
> - *"Which package has the most critical vulnerability?"*
> - *"What should I upgrade first?"*

---

## Tech Stack

| Layer | Tool |
|---|---|
| UI | Streamlit |
| Vulnerability Data | OSV.dev Batch API |
| LLM | Groq (`openai/gpt-oss-120b`) |
| Repo Cloning | GitPython |
| Dependency Parsing | Custom parsers for `.txt`, `.toml`, `.json` |

---

## Project Structure

```
OpenSourceGuardian/
├── app/
│   ├── ingestion/
│   │   ├── clone_repo.py              # Clones GitHub repo
│   │   ├── detect_language.py         # Detects project language
│   │   ├── dependency_file_finder.py  # Finds dependency files
│   │   └── parser.py                  # Parses requirements/package files
│   ├── vulnerability/
│   │   └── osv_client.py              # Queries OSV.dev API
│   ├── llm/
│   │   ├── llm_client.py              # Groq LLM client
│   │   └── prompt.py                  # Prompt builder
│   └── services/
│       └── repository_service.py      # Orchestrates the full scan
├── ui.py                              # Streamlit app
├── main.py                            # CLI entry point
└── pyproject.toml
```

---

## Run Locally

**1. Clone the repo**
```bash
git clone https://github.com/your-username/OpenSourceGuardian.git
cd OpenSourceGuardian
```

**2. Create a virtual environment**
```bash
python -m venv .venv
.venv\Scripts\activate      # Windows
source .venv/bin/activate   # Mac/Linux
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Add your API key**

Create a `.env` file:
```
GROQ_API_KEY=your_groq_api_key_here
```
Get a free key at [console.groq.com](https://console.groq.com)

**5. Run**
```bash
streamlit run ui.py
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key (required) |

---

## Supported Languages

| Language | Dependency File |
|---|---|
| Python | `requirements.txt`, `pyproject.toml` |
| JavaScript | `package.json` |

---

## License

MIT
