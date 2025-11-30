# Smart Task Analyzer

A mini-application built with **Django** that scores and prioritizes tasks using urgency, importance, effort, and dependencies.

---

## 🚀 Features
- POST `/api/tasks/analyze/` — scores and sorts a JSON list of tasks.
- POST `/api/tasks/suggest/` — returns top 3 suggested tasks.
- Simple static frontend at `/static/index.html`.

---

## ⚡ Quick Start (Local Setup)

## Setup Instructions

Follow these steps to run the Smart Task Analyzer locally:

### Clone the Repository
```powershell
git clone https://github.com/asifshaik878/task-analyzer.git
cd task-analyzer


### 1. Create and Activate Virtual Environment
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1

### 2. Install Dependencies
```powershell
pip install -r requirements.txt

### 3. Apply Migrations
```powershell
python manage.py migrate

### 4. Run the Development Server
python manage.py runserver

Open the frontend UI in your browser:
👉 http://127.0.0.1:8000/static/index.html



## 📌 ** Algorithm Explanation (300–500 words)**  
Add this under **“Algorithm Explanation”**:

```markdown
## Algorithm Explanation (300–500 words)

The Smart Task Analyzer is built with the goal of helping users decide which task they should work on first. The scoring algorithm combines four key factors: urgency, importance, estimated effort, and dependencies. These factors represent realistic considerations people use when planning their workday and are designed to capture both short-term deadlines and strategic long-term value.

### 1. Urgency
Urgency is determined by comparing the current date with the task's due date. If the task has no due date, urgency is treated as neutral. If a task is overdue, it receives a large priority boost because overdue work typically causes the most impact. Tasks due within a short window (for example, the next 1–3 days) also receive increased priority, because they require immediate attention. This mirrors real-world decision making where deadlines heavily influence task choice.

### 2. Importance
Importance is a user-supplied rating, usually between 1 and 10. This score represents the intrinsic value or impact of the task. For example, a task with high importance might contribute to a major project milestone or directly affect users. To ensure importance meaningfully affects the final score, it is multiplied by a fixed weight (e.g., ×5). This prevents small urgency differences from overpowering highly important tasks.

### 3. Estimated Effort
Effort represents the number of hours required to complete the task. Short tasks (“quick wins”) receive a small bonus, because users often benefit from completing small tasks early to gain momentum. Larger tasks do not lose points, but they do not receive the quick-win bonus. This reflects a balance between productivity psychology and practical workload planning.

### 4. Dependencies
Tasks can depend on other tasks. If a task cannot be started until another task is completed, its priority is reduced or flagged. Before scoring, the algorithm performs cycle detection to identify circular dependencies (A depends on B, B depends on A). Cycles are highlighted so users can fix the dependency chain before making planning decisions.

### 5. Final Score
Each factor contributes a weighted score:
- Urgency weight
- Importance weight
- Quick-win bonus
- Dependency penalty or flag

The final score is a sum of these components. Higher score = higher priority. The approach blends objective rules (dates, numbers) with subjective user input (importance), producing rankings that feel both logical and intuitive. Overall, the algorithm is designed to be explainable, predictable, and easy to adjust in the future.


## Design Decisions

1. **Django as the Backend Framework**  
   Django was chosen because it provides a clean structure, built-in routing, automatic admin setup, and easy JSON handling without needing external plugins. It also allows future extension into database persistence.

2. **Stateless API Instead of Database Storage**  
   Tasks are analyzed directly from the JSON input rather than saved in the database. This keeps the system simple and avoids unnecessary CRUD complexity for this assignment.

3. **Custom Scoring File (`scoring.py`)**  
   Keeping the scoring logic in a separate file isolates business logic from the views and makes testing easier. It also supports future swapping or tuning of the algorithm.

4. **Frontend Built with Plain HTML/CSS/JS**  
   The assignment required no framework like React, so a minimal static frontend was chosen. This makes loading fast and keeps the focus on backend intelligence.

5. **Human-Readable Explanations**  
   Instead of returning only numbers, the API produces explanations for each score. This improves transparency and helps users understand why one task ranks higher than another.

6. **Cycle Detection for Dependencies**  
   Circular dependencies can break planning in real workflows. Implementing cycle detection ensures the system warns users instead of silently producing incorrect results.


## Time Breakdown

| Task Section                    | Time Spent |
|--------------------------------|------------|
| Project setup (Django + app)   | 45 minutes |
| Building models & URL routing  | 30 minutes |
| Scoring algorithm design       | 1 hour     |
| Implementing analyze/suggest   | 45 minutes |
| Debugging & testing            | 1 hour     |
| Frontend HTML/CSS/JS           | 1 hour     |
| Documentation (README, DEPLOY) | 45 minutes |
| Total                          | ~6 hours   |


## Bonus Challenges Attempted

- ✔ Implemented human-readable explanations for each score.  
- ✔ Implemented circular dependency detection.  
- ✔ Added optional quick-wins logic for short tasks.  
- ✔ Added `/suggest/` endpoint to recommend top 3 tasks.  
- ✔ Added Waitress + Whitenoise deployment steps.


## Future Improvements

- Add user authentication and saved task lists.
- Improve scoring using machine learning or historical completion behavior.
- Add category tags, labels, and grouping logic.
- Build a more advanced frontend with drag-and-drop task cards.
- Add visual charts showing urgency vs importance.
- Add a calendar view for deadline visualization.
- Add bulk import from CSV/Excel or Google Tasks API.







