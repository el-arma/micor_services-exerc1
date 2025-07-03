from fastapi import FastAPI, HTTPException
import uvicorn
import requests
import os
from dotenv import load_dotenv
from db import create_tables, get_orders_from_db, save_order_to_db, get_db_session
from schemas import OrderSchema
import logging
from rich.logging import RichHandler
from sqlalchemy import text
from typing import Any

# Setup Rich logging
logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%X]",
    handlers=[RichHandler(rich_tracebacks=True)]
    )

logger = logging.getLogger("lunchbox")

# Load environment variables from .env file
load_dotenv()

RECOMMENDATION_SERVICE_URL: str = os.getenv("RECOMMENDATION_SERVICE_URL")

def lifespan(_):
    logger.info("🚀  FASTAPI Startup")

    hc_res: dict = health_check()

    if hc_res['status'] == 'ok':
        logger.info("✅ Microservices up and running")

    yield

    logger.info("✖️  FASTAPI Shutdown")

app = FastAPI(lifespan=lifespan)

# Create database tables on startup
create_tables()

@app.get("/")
def root():
    return {"message": "Hello there!"}

@app.get("/orders")
def get_orders() -> dict[str, Any]:
    # Read and return all orders from db using dedicated function
    return {"orders": get_orders_from_db()}

@app.post("/orders")
def take_orders(order_data: OrderSchema) -> dict[str, str]:
    # Save to database
    save_order_to_db(order_data)

    logger.info(f"💾 Order saved order to DB")

    return {"status": "success", "message": "Order saved"}


@app.get("/recommendation")
def get_recommendation():
    try:
        response = requests.get(RECOMMENDATION_SERVICE_URL)
        return response.json()
    except requests.RequestException as exc:
        raise HTTPException(status_code=502, detail=f"Recommendation service error: {exc}")

@app.get("/health")
def health_check() -> dict[str, Any]:
    
    # Check DB connection
    try:
        with get_db_session() as session:
            result: int = session.execute(text("SELECT 1")).scalar()
            if result != 1:
                raise Exception(f"Unexpected DB response: {result}")
        logger.info("✅ Database connection OK")
    except Exception as db_exc:
        logger.error(f"❌ Database connection failed: {db_exc}")
        return {"status": "error", "detail": f"Database error: {db_exc}"}, 500

    # Check Microservice C
    try:
        resp = requests.get(RECOMMENDATION_SERVICE_URL, timeout=2)
        resp.raise_for_status()

        # Check if response has content
        if not resp.content:
            raise Exception("Microservice C returned empty response")
        
        logger.info("✅ Microservice C reachable and returned data")

    except Exception as svc_exc:
        logger.error(f"❌ Microservice C unreachable: {svc_exc}")
        return {"status": "error", "detail": f"Microservice C error: {svc_exc}"}, 502

    return {"status": "ok"}


if __name__ == "__main__":
    uvicorn.run("main:app", host = "127.0.0.1", port = 8000, reload = True)


