from celery import Celery
from celery.utils.log import get_task_logger
from dotenv import load_dotenv
import motor.motor_asyncio
import os

load_dotenv()

client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_CONN"))
database = client.expenses
expenses_collection = database.get_collection("expenses_collection")

celery = Celery('Lunch Expense Service', broker=os.getenv('RABBITMQ_CONN'))
celery_log = get_task_logger(__name__)


@celery.task
async def aggregation_per_place(lunch_location: str) -> str:
    total = []
    async for expense in expenses_collection.find({"lunch_place_name": lunch_location}):
        total.append(expense['amount'])
    return sum(total)