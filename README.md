# FastAPI E-commerce Backend (demo)

---
## Overview
一個基於FastAPI的簡單電商後端，包含註冊、登入、下單，
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

---

## What I learned
- Designing a FastAPI project structure
- Implementing JWT-based authentication
- Applying transaction control in service layer
- Handling database migrations with Alembic
- Securing APIs by rate limiting and CORS
- Depolying backend services with Docker and Nginx
  