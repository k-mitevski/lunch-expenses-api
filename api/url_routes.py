from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder
from api.tasks import aggregation_per_place
from api.models import AddLunchExpense
from api.database import (
    retrieve_expenses,
    add_new_expense,
    retrieve_per_employee
)

router = APIRouter()


@router.get("/", response_description="Retrieved all available lunch expenses!")
async def all_lunch_expenses():
    lunch_expenses = await retrieve_expenses()
    if lunch_expenses:
        return lunch_expenses
    raise HTTPException(status_code=404, detail="Failed to retrieve lunch expenses!")


@router.get("/{employee_name}/{month}", response_description="Successfully fetched monthly lunch expenses!")
async def lunch_per_employee(employee_name: str, month: str):
    lunch_expenses = await retrieve_per_employee(employee_name, month)
    if lunch_expenses:
        return lunch_expenses
    raise HTTPException(status_code=404, detail="Failed to retrieve monthly expenses!")


@router.post("/", response_description="New lunch expense added!")
async def add_lunch_expense(req: AddLunchExpense = Body(...)):
    new_expense = jsonable_encoder(req)
    lunch_place = new_expense['lunch_place_name']

    # Celery part
    total_expenses = aggregation_per_place.delay(lunch_place)
    get_total_expenses = total_expenses.get()

    added_lunch_expense = await add_new_expense(new_expense)
    if added_lunch_expense:
        return f'Total money spent at {lunch_place}: ${get_total_expenses}', added_lunch_expense
    raise HTTPException(status_code=404, detail="Failed to add new lunch expense!")

