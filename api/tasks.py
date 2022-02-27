from celery import Celery
from celery.utils.log import get_task_logger
from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()

client = MongoClient(os.getenv("MONGO_CONN"))
db = client.expenses
expenses_collection = db.get_collection("expenses_collection")

celery = Celery(__name__,
                broker=os.getenv('RABBITMQ_CONN'),
                backend=os.getenv('MONGO_CONN')
                )

celery_log = get_task_logger(__name__)


@celery.task
def aggregation_per_place(lunch_location: str) -> str:
    total = []
    for expense in expenses_collection.find({"lunch_place_name": lunch_location}):
        total.append(expense['amount'])
    return sum(total)
