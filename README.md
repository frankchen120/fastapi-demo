# FastAPI Backend Demo (GCP / Docker)

---
## Overview
一個基於Python/FastAPI的簡單後端，包含註冊、登入、下單，
以 JWT 做認證，登入有 rate limit，整個系統用 Docker 部署。

---
## Tech stack
- Language: Python3
- Backend Framework: FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy
- Migration: Alembic
- Authentication: JWT(OAuth2 Password)
- Security
  - Password hashing
  - Rate limiting on auth endpoints
  - CROS configurations
- Deployment:
  - Docker/Docker Compose
  - Nginx

---
### Key Features
- JWT-based authentication
- Rate limiting on authentication endpoints
- Database schema migration with Alembic
- Health and readiness checks for service startup
- Structured logging and basic error handling
- Containerized deployment with Docker Compose
  
---
## How to Run (Docker)
```
# build and start services
docker compose up --build

# apply database migration
docker compose exec api alembic upgrade head
```

API available at:
```
https://localhost
```

Swagger UI:
```
https://localhost/docs
```
Example APIs:
- POST /auth/register
- POST /auth/login
- GET /auth/me
- POST /orders/me
- GET /orders/me/orders
