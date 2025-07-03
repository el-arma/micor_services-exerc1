from db import Base
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from schemas import OrderSchema

# Test database configuration
TEST_DATABASE_URL = "sqlite:///./test.db"  # In-memory SQLite for testing

@pytest.fixture(scope="function")
def test_db():
    """
    Create a fresh test database for each test.
    Uses SQLite in-memory database for speed.
    """
    
    # Create test engine
    engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestSessionLocal()
    
    yield session
    
    # Cleanup
    session.close()
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def sample_order():
    """Sample order data for testing."""
    return OrderSchema(user_id=1, lunch_item="Test Pizza")

@pytest.fixture
def sample_order_dict():
    """Sample order as dictionary for testing."""
    return {"user_id": 1, "lunch_item": "Test Pizza"}
