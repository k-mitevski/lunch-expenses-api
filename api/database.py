from dotenv import load_dotenv
import motor.motor_asyncio
import asyncio
import os

load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_CONN"))
client.get_io_loop = asyncio.get_event_loop
database = client.expenses
expenses_collection = database.get_collection("expenses_collection")


def lunch_helper(expense) -> dict:
    return {
        "id": str(expense["_id"]),
        "employee_name": expense["employee_name"],
        "lunch_place_name": expense["lunch_place_name"],
        "lunch_place_address": expense["lunch_place_address"],
        "food": expense["food"],
        "amount": f'${expense["amount"]}',
        "description": expense["description"],
        "date": expense["date"],
        "receipt": str(expense["receipt"])
    }


async def retrieve_expenses() -> list:
    expenses = []
    async for expense in expenses_collection.find():
        expenses.append(lunch_helper(expense))
    return expenses


async def retrieve_per_employee(employee_name: str, month: str) -> tuple | str:
    expenses = []
    total = []
    # noinspection SpellCheckingInspection
    zfilled = month.zfill(2)
    async for expense in expenses_collection.find({"employee_name": employee_name}):
        if zfilled == expense['date'].split('-')[1]:
            expenses.append(lunch_helper(expense))
        total.append(expense['amount'])
    if not expenses:
        return f"No or error retrieving data for {employee_name} for month {zfilled}."
    return f'{employee_name}\'s total for month {month}: ${sum(total)}', expenses


async def add_new_expense(expense_data: dict) -> dict:
    expense = await expenses_collection.insert_one(expense_data)
    new_expense = await expenses_collection.find_one({"_id": expense.inserted_id})
    return lunch_helper(new_expense)
