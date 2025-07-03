import pytest
from unittest.mock import patch, MagicMock

# Import from parent directory
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from db import save_order_to_db, get_orders_from_db, Order
from schemas import OrderSchema

class TestDatabaseOperations:
    """Test database functions without hitting the real database."""
    
    @patch('db.get_db_session')
    def test_save_order_to_db_success(self, mock_session, sample_order):
        """Test saving an order successfully."""
        # Mock the database session
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        # Mock the new order
        mock_order = MagicMock()
        mock_order.id = 42
        mock_db.query.return_value.filter.return_value.first.return_value = None
        
        # Mock Order creation
        with patch('db.Order', return_value=mock_order):
            result = save_order_to_db(sample_order)
            
            # Verify database operations were called
            mock_db.add.assert_called_once()
            mock_db.commit.assert_called_once()
            mock_db.refresh.assert_called_once()
    
    @patch('db.get_db_session')
    def test_get_orders_from_db(self, mock_session):
        """Test fetching orders from database."""
        # Mock the database session
        mock_db = MagicMock()
        mock_session.return_value.__enter__.return_value = mock_db
        
        # Mock order data
        mock_order = MagicMock()
        mock_order.id = 1
        mock_order.user_id = 123
        mock_order.lunch_item = "Pizza"
        mock_order.created_at = "2025-07-02"
        
        mock_db.query.return_value.all.return_value = [mock_order]
        
        # Call function
        result = get_orders_from_db()
        
        # Verify result
        assert len(result) == 1
        assert result[0]["id"] == 1
        assert result[0]["user_id"] == 123
        assert result[0]["lunch_item"] == "Pizza"
        
        # Verify database was queried
        mock_db.query.assert_called_once_with(Order)

    def test_order_schema_validation(self):
        """Test that OrderSchema validates data correctly."""
        # Valid data
        valid_order = OrderSchema(user_id=1, lunch_item="Pizza")
        assert valid_order.user_id == 1
        assert valid_order.lunch_item == "Pizza"
        
        # Invalid data should raise validation error
        with pytest.raises(Exception):  # Pydantic validation error
            OrderSchema(user_id="invalid", lunch_item="Pizza")
