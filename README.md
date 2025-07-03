# LunchBoxHub

A FastAPI microservice practice.

## Usage

- **Start PostgreSQL (Docker):**
  ```sh
  docker build -f Service-A/Dockerfile.postgres -t lunchboxhub-db .
  docker run -d -p 5432:5432 --name lunchboxhub-db lunchboxhub-db
  ```
- **Run the API:**
  ```sh
  uvicorn ServiceA.main:app --reload
  ```
- **Run tests (SQLite, no DB needed):**
  ```sh
  cd Service-A
  pytest
  ```

---
- Python 3.12+, FastAPI, SQLAlchemy, Pydantic, Pytest
- Config via `.env` files
