# Miguel Portfolio

Initial Django portfolio structure with separate apps for home, experience, projects, chatbot, contact, and knowledge base.

## Local Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

Health check: `/health/` returns `{"status": "ok"}`.
