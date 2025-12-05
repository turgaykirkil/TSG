# 🔧 Backend API

FastAPI-based backend service for Sicilius platform.

## 🛠 Tech Stack

- FastAPI - Web framework
- SQLAlchemy - ORM
- PostgreSQL + PostGIS - Database
- Redis - Caching
- MinIO - Object storage

## 📂 Structure

```
backend/
├── app/
│   ├── api/          # API endpoints
│   ├── core/         # Core configs
│   ├── models/       # Database models
│   ├── schemas/      # Data schemas
│   └── services/     # Business logic
├── requirements.txt
└── Dockerfile
```

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your settings

# Run migrations
alembic upgrade head

# Start server
uvicorn app.main:app --reload --port 5001
```

## 🐳 Docker

```bash
docker build -t sicilius-backend .
docker run -p 5001:5001 sicilius-backend
```

## 📚 API Docs

Visit http://localhost:5001/docs for interactive API documentation.

## 🔑 Environment Setup

Required environment variables:
- `TSG_DATABASE_URL` - PostgreSQL connection string
- `TSG_SECRET_KEY` - JWT secret key
- `TSG_MINIO_ENDPOINT` - MinIO endpoint
- `TSG_OPENAI_API_KEY` - OpenAI API key (for OCR)

See `.env.example` for complete configuration.

## 🗃️ Database

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1
```

## 📝 License

MIT License
