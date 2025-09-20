## MLOps_A1 — Flask ML App Starter

A minimal Flask web application serving a scikit-learn model trained on a group-unique dataset. Designed for two-member teams (one admin, one member) and prepared for later CI/CD with GitHub, GitHub Actions, Jenkins, and Docker.

### Features
- **/predict** endpoint returning JSON predictions from a pre-trained model
- **Unique dataset per group** via deterministic synthetic generation using a group ID seed
- **Training script** to produce `models/model.pkl` (scikit-learn Pipeline)
- **Pytest** tests for app and model
- **Ready for CI/CD**: Dockerfile, placeholder GitHub Actions, Jenkinsfile

### Tech Stack
- Python 3.10+
- Flask, scikit-learn, pandas, numpy
- pytest

---

## Getting Started

### 1) Create and activate a virtual environment
```bash
python -m venv .venv
./.venv/Scripts/activate  # Windows PowerShell
```

### 2) Install dependencies
```bash
pip install -r requirements.txt
```

### 3) Dataset
This project now uses a provided regression dataset: `data/Salary_dataset.csv` with columns:
- `YearsExperience` (feature)
- `Salary` (target)

### 4) Train the model
```bash
python scripts/train_model.py --data data/Salary_dataset.csv --target Salary --model-out models/model.pkl
```

### 5) Run the Flask app

Windows PowerShell:
```powershell
$env:FLASK_APP = "app:create_app"   # app factory
$env:MODEL_PATH = "models/model.pkl"
flask run --host 0.0.0.0 --port 5000
```

Linux/macOS (bash):
```bash
export FLASK_APP=app:create_app
export MODEL_PATH=models/model.pkl
flask run --host=0.0.0.0 --port=5000
```

Health check:
```powershell
Invoke-RestMethod -Uri http://127.0.0.1:5000/health -Method Get
```

Prediction examples (regression: input is YearsExperience):

Linux/macOS (bash):
```bash
curl -X POST http://127.0.0.1:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"instances": [1.2, 3.0, 10.6]}'
```

Windows PowerShell (recommended):
```powershell
$body = @{ instances = @(1.2, 3.0, 10.6) } | ConvertTo-Json
Invoke-RestMethod -Uri http://127.0.0.1:5000/predict -Method Post -ContentType "application/json" -Body $body
```

Windows PowerShell using curl.exe explicitly (avoid curl alias):
```powershell
C:\Windows\System32\curl.exe -X POST http://127.0.0.1:5000/predict -H "Content-Type: application/json" -d '{"instances":[1.2,3.0,10.6]}'
```

Note: In PowerShell, using single quotes around JSON may prevent proper parsing. Prefer the PowerShell-native example above or ensure proper escaping with double quotes as shown.

---

## Tests
Run unit tests:
```powershell
# Run from the project root (where this README resides)
.\.venv\Scripts\Activate.ps1  # if not already active
pytest -q
```

If you see `ModuleNotFoundError: No module named 'app'`, ensure you run pytest from the project root. This repo includes `pytest.ini` and `tests/conftest.py` to add the project root to `PYTHONPATH` automatically.

---

## Project Structure
```text
.
├── app/
│   ├── __init__.py
│   ├── app.py
│   └── model_utils.py
├── data/
│   └── dataset_GROUP_DEMO.csv
├── models/
│   └── (model.pkl after training)
├── scripts/
│   ├── generate_dataset.py
│   └── train_model.py
├── tests/
│   ├── test_app.py
│   └── test_model.py
├── .github/
│   └── workflows/
│       ├── flake8.yml
│       └── pytest.yml
├── .gitignore
├── Dockerfile
├── Jenkinsfile
├── README.md
└── requirements.txt
```

---

## Dataset
- Regression dataset `data/Salary_dataset.csv` with `YearsExperience` and `Salary`.
- If you replace the dataset, keep the same column names or update `scripts/train_model.py` accordingly.

---

## Assumptions
- Python 3.10+ environment
- Dataset sizes are modest (<= 50k rows) to keep repo light
- Model is a scikit-learn Pipeline: `StandardScaler` + `LogisticRegression`
- Model path defaults to `models/model.pkl` and can be overridden via `MODEL_PATH` env var

### Quick local model check (no server)
PowerShell here-string:
```powershell
@'
import pandas as pd
from app.model_utils import load_model, predict_with_model
model = load_model("models/model.pkl")
df = pd.read_csv("data/dataset_GROUP_DEMO.csv")
X = df.drop(columns=["target"]).head(5)  # keep as DataFrame to avoid sklearn warning
print(predict_with_model(model, X.values.tolist()))
'@ | python -
```

---

## Docker (placeholder)
Build and run locally:
```bash
docker build -t mlops_a1:dev .
docker run -p 5000:5000 -e MODEL_PATH=/app/models/model.pkl mlops_a1:dev
```

---

## GitHub Repository Setup Guide
1) Create a new GitHub repo (private or public) and push this project.
2) Create branches: `dev`, `test`, and `master`.
   - In GitHub UI: Branch dropdown → Create `dev`, then `test`, and ensure `master` exists.
3) Branch protection rules (Settings → Branches → Add rule):
   - Protect `dev`, `test`, `master`: require pull requests, disallow direct pushes.
   - Require at least 1 approving review. Make the admin the code owner/approver.
   - Optionally require status checks (flake8 on PRs to `dev`, pytest on PRs to `test`).
4) Roles and workflow:
   - Admin: repo owner/maintainer with merge rights to `dev`, `test`, `master` via PR approval.
   - Member: works on feature branches, opens PRs to `dev` → after review/approval merge to `dev`.
   - Releases: PR from `dev` → `test` (tests run), then `test` → `master` when stable.

---

## CI/CD Placeholders
- `.github/workflows/flake8.yml`: runs flake8 on PRs to `dev`.
- `.github/workflows/pytest.yml`: runs pytest on PRs to `test`.
- `Jenkinsfile`: placeholder stages for build, test, dockerize, and push.

Configure later to integrate Docker Hub, environment secrets, etc.


this is read me file

