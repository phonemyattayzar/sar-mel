# Project: Sar-Mel (Food Ordering App)
# Status: Development Phase - Backend (Paused)

## ✅ Completed Tasks
- Project structure initialized (FastAPI + Docker + Postgres).
- Database plumbing done (session.py, base_class.py, config.py).
- Security layer implemented (Bcrypt fix with pinned version 3.2.0).
- User Model & Schemas completed.
- User Registration API working (/api/v1/users/).
- Alembic set up and first migration applied (users table).
- API Refactor: Centralized router hub (api.py) with versioned prefixes.

## 🚧 Current Task (Paused)
- **Task 8: Restaurant Entity implementation.**
  - Need to create backend/app/models/restaurant.py.
  - Need to link User <-> Restaurant (One-to-Many relationship).
  - Need to register the new model in backend/app/db/base.py.
  - Need to run Alembic migrations for the new table.

## 📝 Next Steps (For Tomorrow)
1. Implement the Restaurant model with ForeignKeys and SQLAlchemy Relationships.
2. Update User model to support back_populates for restaurants.
3. Generate and run Alembic migration for the restaurants table.
4. Create Restaurant Schemas (Pydantic models) and CRUD logic.
5. Create the Restaurant API endpoints.

---
*Last updated: Thursday, May 28, 2026*
