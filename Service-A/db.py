from contextlib import contextmanager
from datetime import datetime
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from typing import List, Dict, Any
import os


# Load environment variables from .env file
load_dotenv()

# Get PostgreSQL connection string (DSN) from environment variables
DATABASE_URL: str = os.getenv("DATABASE_URL")

# SQLAlchemy setup - create database engine and session factory
engine = create_engine(DATABASE_URL)  # Creates connection to PostgreSQL
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)  # Session factory
Base = declarative_base()  # Base class for all database models

# Orders table model - defines the structure of the 'orders' table
class Order(Base):
    __tablename__ = "orders"  # Name of the table in PostgreSQL
    
    # Primary key - auto-incrementing integer
    id = Column(Integer, primary_key=True, index=True)
    
    # User who made the order - required field
    user_id = Column(Integer, nullable=False)
    
    # What lunch item was ordered - required field
    lunch_item = Column(String, nullable=False)
    
    # When the order was created - automatically set to current UTC time
    created_at = Column(DateTime, default=datetime.now)

# Create tables function - creates all tables if they don't exist
def create_tables():
    """
    Creates all database tables defined in Base.metadata.
    If tables already exist, this does nothing.
    Safe to call multiple times.
    """
    Base.metadata.create_all(bind=engine)


@contextmanager
def get_db_session():
    """
    Context manager for database sessions.
    Automatically handles session creation and cleanup.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Database operations functions
def get_orders_from_db() -> List[Dict[str, Any]]:
    """
    Fetch all orders from the database.
    Returns a list of dictionaries with order data.
    """
    with get_db_session() as db:
        orders = db.query(Order).all()
        return [{"id": row.id, "user_id": row.user_id, "lunch_item": row.lunch_item, "created_at": row.created_at} for row in orders]

def save_order_to_db(order_data):
    """
    Save a new order to the database.
    Returns the created order ID.
    """

    with get_db_session() as db:
        new_order = Order(
            user_id=order_data.user_id,
            lunch_item=order_data.lunch_item
            )

        db.add(new_order)

        db.commit()

        db.refresh(new_order)
        
        return None
