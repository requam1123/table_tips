from fastapi import FastAPI
from pydantic import BaseModel
from typing import List

app = FastAPI()

all_tips = []

class Tip(BaseModel):
    title : str
    ddl : str
    uuid : str
    group : str
    cdate : str

@app.get("/")
def read_root():
    return{"message": "🎉 Tip Server is running!"}

@app.get("/tips",response_model= List[Tip])
def get_tips():
    return all_tips

@app.post("/tips")
def add_tips(tip:Tip):
    all_tips.append(tip)
    return {"message": "已添加 tip", "tip": tip}