# 🚀 AutoDocGen

## 📌 Overview
AutoDocGen is an AI-powered documentation generator that automatically analyzes code changes between Git commits and produces human-readable explanations.

It extracts the difference between the latest and previous commit, sends the changes to an AI model, and generates structured documentation saved as a text file. This eliminates the need for manual documentation and helps developers quickly understand how code evolves over time.

---

## ⚙️ Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 2. Add Mistral API Key

Open `docgen.py` and add your API key:

```python
apikey = "YOUR_MISTRAL_API_KEY"
```

---

## ⚙️ Usage

AutoDocGen can be used in two modes:

### 🟢 1. MANUAL Mode
Run the script manually after making commits:

```bash
python docgen.py --manual
```

- Analyzes changes between the latest and previous commit  
- Generates documentation  
- Saves output in `document.txt`  

---

### 🔵 2. GitHub Pipeline Mode (Automated)

Run the script once:

```bash
python docgen.py
```

- Automatically creates a GitHub Actions workflow file  
- On every `git push`:
  - Pipeline runs automatically  
  - Executes the script  
  - Generates documentation  
  - Commits the generated `document.txt` back to the repository  

---



---
