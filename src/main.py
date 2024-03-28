from fastapi import FastAPI
from pydantic import BaseModel

import src.model



class Request(BaseModel):
    text: str
    lead_id: int


app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.post("/response/")
async def submit_request(req: Request):
    print(req)
    return model.Model().f(req)
