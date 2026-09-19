# AI-Enhanced Company Alumni Portal

Full-stack alumni portal for the Gradious project.

## Features
- Alumni registration and login
- HR/Admin login
- Alumni profile management
- Alumni directory and search
- Company news and updates
- Event management
- Messaging
- Dashboard
- KNN alumni connection recommendations
- Generative AI networking summaries
- AI event invitations
- AI professional messages
- AI engagement insights

## Stack
Frontend: HTML, CSS, JavaScript
Backend: Flask REST API
Database: SQLite (easy demo setup; replaceable with MySQL)
ML: scikit-learn KNN
GenAI: OpenAI-compatible API with local fallback

## Run
1. `python -m venv venv`
2. Windows: `venv\Scripts\activate`
3. `pip install -r requirements.txt`
4. `python ML/train_model.py`
5. `python Backend/app.py`
6. Open http://127.0.0.1:5000

Demo:
Alumni: alumni@gradious.com / alumni123
Admin: admin@gradious.com / admin123

Optional GenAI:
Set `OPENAI_API_KEY` and optionally `OPENAI_MODEL`.
Without a key, the project uses a local fallback so the portal still works.
