# Family Chat MVP

A simple full-stack private family chat application built with FastAPI, SQLite, JWT auth, and vanilla JavaScript.

## Features

- User registration and login with JWT authentication
- Password hashing with bcrypt
- SQLite database via SQLAlchemy
- Chat list for the authenticated user
- Message history for selected chat
- Send text and image messages
- File uploads saved to local `/uploads` directory
- Frontend polling every 2.5 seconds for new messages

## Project structure

```
.
├── main.py
├── database.py
├── models/
│   ├── user.py
│   ├── chat.py
│   ├── chat_user.py
│   └── message.py
├── routes/
│   ├── auth.py
│   ├── chats.py
│   ├── messages.py
│   └── upload.py
├── utils/
│   ├── auth.py
│   └── deps.py
├── static/
│   ├── index.html
│   ├── api.js
│   ├── login.js
│   └── chat.js
├── uploads/
└── requirements.txt
```

## API endpoints

- `POST /register`
- `POST /login`
- `GET /chats`
- `GET /messages?chat_id=...`
- `POST /messages`
- `POST /upload`

## Setup

1. Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
uvicorn main:app --reload
```

4. Open in browser:

- http://127.0.0.1:8000

## Notes

- A default chat named `Family` is created automatically.
- Each newly registered user is added to the `Family` chat.
- Uploaded files are available under `/uploads/<filename>`.
- This is an MVP for local development (not production hardened).
