from fastapi import FastAPI
from api.url_routes import router as ExpenseRouter

app = FastAPI(title="Lunch Expenses API")
app.include_router(ExpenseRouter, tags=["Lunch Expenses"], prefix="/lunch")

