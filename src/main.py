from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from src.processors import processor1, processor2

app = FastAPI()

class MessageRequest(BaseModel):
    body: str
    from_: str = Field(..., alias='from')
    to_: str = Field(..., alias='to')

@app.post("/process_message")
async def process_message(request: MessageRequest):
    body = request.body
    to_ = request.to_

    if to_ == "62811334932@c.us":
        return await processor1.process_message(body)
    elif to_ == "6282312132187@c.us":
        return await processor2.process_message(body)
    else:
        raise HTTPException(status_code=204)  # No Content

@app.get("/")
async def root():
    return {"message": "FastAPI WhatsApp is running on port 8000 🌟"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)