from fastapi import FastAPI
from models import User

app = FastAPI()

@app.get("/user/{id}")
async def get_users(id):
    print('Starting')
    data = User.model_dump()
    print(data)
    return {"id": id, **data}

@app.get("/")
async def root():
    return {"message": "Hello World"}