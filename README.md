# FastAPI Playground

My playground for learning and experimenting with FastAPI.

## Requirements

- Python 3.8+
- pip

## Installation

1. **Clone the repository**

   ```bash
   git clone git@github.com:ujangdoubleday/fastapi-playground.git
   cd fastapi-playground
   ```

2. **Create a virtual environment**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the App

Start the development server:

```bash
fastapi dev
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## Database Setup

The project is configured to use **SQLite**. The database file (`sql_app.db`) and tables are **automatically created** when you start the application for the first time.

You don't need to run any manual migration commands for this initial setup.

## API Documentation

FastAPI provides automatic interactive documentation. Once the app is running, visit:

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## Official Documentation

- **FastAPI Documentation**: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- **SQLAlchemy Documentation**: [https://docs.sqlalchemy.org/](https://docs.sqlalchemy.org/)
- **Pydantic Documentation**: [https://docs.pydantic.dev/](https://docs.pydantic.dev/)

## Project Structure

```
.
├── app
│   ├── api
│   │   ├── deps.py      # Dependencies (e.g., gets_db)
│   │   └── v1
│   │       ├── api.py   # Main router for v1
│   │       └── endpoints
│   ├── db
│   │   ├── base.py      # Declarative base
│   │   └── session.py   # Database session configuration
│   ├── models           # SQLAlchemy models
│   ├── schemas          # Pydantic schemas
│   └── main.py          # App entry point
├── requirements.txt
└── README.md
```
