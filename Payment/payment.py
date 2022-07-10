from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel
from starlette.requests import Request
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

# this should be different db
redis = get_redis_connection(
    host="redis-13946.c55.eu-central-1-1.ec2.cloud.redislabs.com",
    port=13946,
    password="qJaiUPU2TpITAlCyrKkqxb4VDULQH0lR",
    decode_responses=True
)

class Order(HashModel):
    product_id: str
    price: float
    fee: float
    total: float
    quantity: int
    status: str

    class Meta:
        database = redis

@app.post('/orders')
async def create(request: Request):
    body = await request.json()

    req = requests.get('http://localhost:8000/products/%s' % body)


