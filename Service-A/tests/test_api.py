from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app

# Create test client
client = TestClient(app)

class TestAPIEndpoints:
    """Test FastAPI endpoints."""
    
    def test_root_endpoint(self):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        assert response.json() == {"message": "Hello there!"}
    
    @patch('main.get_orders_from_db')
    def test_get_orders_endpoint(self, mock_get_orders):
        """Test GET /orders endpoint."""
        # Mock the database function
        mock_get_orders.return_value = [
            {"id": 1, "user_id": 123, "lunch_item": "Pizza", "created_at": "2025-07-02"}
        ]
        
        response = client.get("/orders")
        
        assert response.status_code == 200
        data = response.json()
        assert "orders" in data
        assert len(data["orders"]) == 1
        assert data["orders"][0]["lunch_item"] == "Pizza"
        
        # Verify mock was called
        mock_get_orders.assert_called_once()
    
    @patch('main.save_order_to_db')
    def test_post_orders_endpoint(self, mock_save_order):
        """Test POST /orders endpoint."""
        # Mock the database function
        mock_save_order.return_value = 42
        
        order_data = {"user_id": 1, "lunch_item": "Test Pizza"}
        
        response = client.post("/orders", json=order_data)
        
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "success"
        assert data["message"] == "Order saved"
        
        # Verify mock was called
        mock_save_order.assert_called_once()
    
    def test_post_orders_invalid_data(self):
        """Test POST /orders with invalid data."""
        invalid_data = {"user_id": "invalid", "lunch_item": "Pizza"}
        
        response = client.post("/orders", json=invalid_data)
        
        assert response.status_code == 422  # Validation error
    
    @patch('main.requests.get')
    def test_get_recommendation_success(self, mock_requests):
        """Test GET /recommendation endpoint success."""
        # Mock successful recommendation service response
        mock_response = MagicMock()
        mock_response.json.return_value = {"recommendation": "Sushi"}
        mock_requests.return_value = mock_response
        
        response = client.get("/recommendation")
        
        assert response.status_code == 200
        assert response.json() == {"recommendation": "Sushi"}
    

