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

## Testing

This project uses `pytest` for automated testing.

```bash
pytest
```

This runs all tests in the `tests/` directory using an in-memory database.

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

## Configuration

Create a `.env` file for local development (see `.env.example`):

```bash
cp .env.example .env
```

Key settings:

- `SECRET_KEY`: Use `openssl rand -hex 32` to generate one.
- `ALGORITHM`: Default is HS256.
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token validity duration.

You can also use **OS environment variables**, which take precedence over `.env` files:

```bash
export SECRET_KEY="super_secret_from_os"
fastapi run
```

For more details, see the [FastAPI Environment Variables Documentation](https://fastapi.tiangolo.com/environment-variables/).

## Authentication (v2)

The `v2` API implements JWT Authentication.

### 1. Register

`POST /api/v2/auth/signup`

### 2. Login

`POST /api/v2/auth/login`

- Uses OAuth2 Password Request Form.
- **Username**: Enter your **Email**.
- **Password**: Enter your password.

### 3. Protected Routes

Use the returned `access_token` in the Authorization header: `Bearer <token>`.

## Project Structure

```
.
├── app
│   ├── api
│   │   ├── deps.py      # Dependencies (e.g., gets_db)
│   │   ├── v1           # Open endpoints
│   │   └── v2           # Authenticated endpoints (JWT)
│   ├── core             # Config and Security
│   │   ├── config.py
│   │   └── security.py
│   ├── db
│   │   ├── base.py      # Declarative base
│   │   └── session.py   # Database session configuration
│   ├── models           # SQLAlchemy models
│   ├── schemas          # Pydantic schemas
│   └── main.py          # App entry point
├── requirements.txt
└── README.md
```
