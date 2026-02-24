from fastapi import FastAPI, Request, Response, HTTPException
from models import User
import json
import toggl as tg
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/user/{id}")
async def get_users(id):
    print('Starting')
    data = User.model_dump()
    print(data)
    return {"id": id, **data}

@app.post("/toggl/time_entry")
async def handle_time_entry(request: Request):
    req = await request.json()
    is_ping = req['payload'] == 'ping'
    message = json.dumps(req, separators=(",", ":"))
    headers = request.headers
    signature = headers['x-webhook-signature-256'] if 'x-webhook-signature-256' in headers else None
    secret = os.getenv('TG_SECRET')

    if tg.validate(message, signature, secret):
        print("Toggl request validated")
    else:
        print("Toggl request could not be validated")
        raise HTTPException(status_code=403, detail="The request was not validated")
    
    if is_ping:
        print("Validating Endpoint")
        validation_code = req['validation_code'] if 'validation_code' in req else None
        if not validation_code:
            print("Pong!")
            return "Pong!"
        return Response(content=json.dumps({"validation_code": validation_code}), media_type='application/json')
    else:
        try:
            payload = req['payload']
            tg.update_time_entries({
                "record_status": "Deleted" if req['metadata']['action'] == 'deleted' else 'Active',
                "toggl_id": payload['id'],
                "description": payload['description'],
                "project_id": payload['project_id'],
                "start": payload['start'],
                "stop": payload['stop'],
                "tags": ", ".join(payload['tags']) if payload['tags'] else None,
                "user_id": payload['user_id']
            })
        except Exception as e:
            print(e)
            raise HTTPException(status_code=500, detail="Internal Server Error")
    
    return 'OK'

@app.get("/")
async def root():
    return {"message": "Hello World"}