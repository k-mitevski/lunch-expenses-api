# Lunch Expenses API
Lunch expenses API using FastAPI, Celery, RabbitMQ, and MongoDB.

![](https://i.imgur.com/eCcsutS.png)


## Install and running the app
Create a venv (or don't), install the libraries and run the `main.py`. [Uvicorn](https://www.uvicorn.org/) is used as the ASGI to run the app.

The `MONGO_CONN` and `RABBITMQ_CONN` environment variables are used to pass the connection strings.
```
pip install -r requirements.txt
```
```
python main.py
```

To run the Celery worker:
```
cd celery_code
celery -A celery_worker.celery worker --loglevel=info
```

The API currently has three types of requests all available on `/lunch` path.

## GET

### Get all available lunch expenses
```
curl -H 'accept: application/json' http://localhost:5000/lunch/
[
  {
    "id": "6218ff66a05ed4306c4e162e",
    "employee_name": "John Doe",
    "lunch_place_name": "Some lunch bar",
    "lunch_place_address": "Kej",
    "food": "Pizza",
    "amount": "$8.0",
    "description": "Lunch break...",
    "date": "2022-02-25T16:03:25.914981",
    "receipt": "None"
  },
  {
    "id": "6218ff86a05ed4306c4e162f",
    "employee_name": "John Doe",
    "lunch_place_name": "Mcdonalds",
    "lunch_place_address": "Kej",
    "food": "Cheeseburger",
    "amount": "$2.5",
    "description": "Lunch break...",
    "date": "2022-02-25T16:03:25.914981",
    "receipt": "None"
  }
]
```

### Get lunch expenses per month for specific employee

The request is sent using path parameters. `/lunch/{employee_name}/{month}`
The response will include total amount spent in that particular month. 

Example for employee John Doe for February:
```
curl -H 'accept: application/json' http://localhost:5000/lunch/John%20Doe/2
[
  "John Doe's total for month 2: $10.5",
  [
    {
      "id": "6218ff66a05ed4306c4e162e",
      "employee_name": "John Doe",
      "lunch_place_name": "Some lunch bar",
      "lunch_place_address": "Kej",
      "food": "Pizza",
      "amount": "$8.0",
      "description": "Lunch break...",
      "date": "2022-02-25T16:03:25.914981",
      "receipt": "None"
    },
    {
      "id": "6218ff86a05ed4306c4e162f",
      "employee_name": "John Doe",
      "lunch_place_name": "Mcdonalds",
      "lunch_place_address": "Kej",
      "food": "Cheeseburger",
      "amount": "$2.5",
      "description": "Lunch break...",
      "date": "2022-02-25T16:03:25.914981",
      "receipt": "None"
    }
  ]
]
```
## POST
One HTTP POST request is available for adding lunch expenses.

When new expense is added, a task is triggered with Celery to calculate the total money spent at the lunch expense location.

Example request:
```
curl -X 'POST' http://localhost:5000/lunch/' -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "employee_name": "John Doe",
  "lunch_place_name": "Mcdonalds",
  "lunch_place_address": "Kej",
  "food": "Hamburger",
  "amount": 2,
  "description": "Lunch break..."
}'
[
  "Total money spent at Mcdonalds: $10.5",
  {
    "id": "621b9b20f2c33dac50c2e89c",
    "employee_name": "John Doe",
    "lunch_place_name": "Mcdonalds",
    "lunch_place_address": "Kej",
    "food": "Hamburger",
    "amount": "$2.0",
    "description": "Lunch break...",
    "date": "2022-02-27T15:39:03.954968",
    "receipt": "None"
  }
]
```