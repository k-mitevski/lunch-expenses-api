from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime


class AddLunchExpense(BaseModel):
    employee_name: str = Field(..., exclusiveMinimum=2)
    lunch_place_name: str = Field(..., exclusiveMinimum=2, description="The name of the place")
    lunch_place_address: str | None = Field(description="Address of the place")
    food: str = Field(..., exclusiveMinimum=0, description="What was eaten for lunch")
    amount: float = Field(..., gt=0)
    description: str = Field(..., exclusiveMaximum=50, description="Description of the occasion")
    date: datetime | None = datetime.utcnow()
    receipt: HttpUrl | None = None

    class Config:
        schema_extra = {
            "example": {
                "employee_name": "John Doe",
                "lunch_place_name": "Soul Kitchen",
                "lunch_place_address": "Kej",
                "food": "Cheeseburger",
                "amount": 4.5,
                "description": "Lunch break...",
            }
        }
