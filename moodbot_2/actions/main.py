from fastapi import FastAPI, Depends, Response
from schemes import Message
from resources import load_rasa_model
import requests

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Welcome World"}

@app.post("/nlu/parse")
async def chatbot_parse(message: Message, response: Response, model=Depends(load_rasa_model)):
    if message.text.strip() == "":
        response.status_code = 400
        return {"error": "You must provide a text"}

    pred = await model.parse_message(message_data=message.text)
  
    return {"results": pred}
