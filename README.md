# Smart Task Analyzer

A mini-application built with **Django** that scores and prioritizes tasks using urgency, importance, effort, and dependencies.

---

## 🚀 Features
- POST `/api/tasks/analyze/` — scores and sorts a JSON list of tasks.
- POST `/api/tasks/suggest/` — returns top 3 suggested tasks.
- Simple static frontend at `/static/index.html`.

---

## ⚡ Quick Start (Local Setup)

### 1. Create & Activate Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
