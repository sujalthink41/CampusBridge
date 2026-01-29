# CampusConnect Backend

Backend service for **CampusConnect** — a college–alumni–student engagement platform that enables verified users to share updates, provide career guidance, and communicate securely within their institution.

---

## Tech Stack

- **Backend Framework**: FastAPI
- **ASGI Server**: uv (uvicorn-compatible)
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Auth**: Role-based access (Student / Alumni / College Official / Admin)
- **Storage**: AWS S3 (ID card & document uploads)

---

## Features (v1)

- College-based user onboarding & verification
- Student, Alumni & College Official role management
- Admin verification via ID cards
- College feed (posts & comments)
- Alumni guidance requests & 1:1 chat
- Notification system

---

## Project Setup

git clone <repo-url>
cd server
install dependencies : uv sync
run server : uv run poe dev


How to use it:
Make changes to models -> Run uv run alembic revision --autogenerate -m "message"
Apply changes -> Run uv run alembic upgrade head
