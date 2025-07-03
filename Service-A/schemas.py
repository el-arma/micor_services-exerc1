from pydantic import BaseModel

class OrderSchema(BaseModel):
    user_id: int
    lunch_item: str