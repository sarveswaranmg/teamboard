# TeamBoard API

TeamBoard is a Django REST Framework backend for an AI-powered Knowledge Base platform.

Companies can register and receive an API key, authenticate using JWT, search the knowledge base, and have their queries tracked for usage analytics. Platform administrators can view usage statistics and the most frequently searched terms.

---

## Features

- Company registration
- Automatic API key generation
- JWT authentication using SimpleJWT
- Company login
- Knowledge Base search
- Case-insensitive search across questions and answers
- Query usage logging
- Atomic database transactions
- Custom admin-only permission
- Platform-wide usage summary
- Top 5 most searched terms
- PostgreSQL database
- Docker-based PostgreSQL setup
- Postman API collection

---

## Tech Stack

- Python
- Django
- Django REST Framework
- SimpleJWT
- PostgreSQL
- Docker
- python-dotenv
- Postman

---

## Project Structure

```text
teamboard/
│
├── api/
│   ├── migrations/
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── permissions.py
│   ├── serializers.py
│   ├── signals.py
│   ├── urls.py
│   └── views.py
│
├── teamboard/
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── .env
├── .gitignore
├── compose.yml
├── manage.py
├── requirements.txt
├── TeamBoard.postman_collection.json
└── README.md