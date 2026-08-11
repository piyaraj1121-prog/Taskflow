# TaskFlow

TaskFlow is a FastAPI + SQLAlchemy task management application with a
HTML/CSS/JavaScript dashboard.

The project contains:

- FastAPI backend
- SQLAlchemy database layer
- Task CRUD APIs
- Statistics endpoint
- Priority sorting
- Binary-search based task search
- Algorithm implementations and benchmarks
- AI Quick Add using a zero-key mock parser by default
- Optional Groq integration behind `USE_GROQ=true`

---

## Project Structure

```text
TaskFlow/
├── backend/
│   ├── ai_service.py
│   ├── algorithms/
│   │   └── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   ├── routes.py
│   ├── schemas.py
│   └── requirements.txt
│
├── frontend/
│   ├── app.js
│   ├── index.html
│   └── style.css
│
├── benchmark.py
├── check_algorithms.py
└── README.md