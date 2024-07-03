from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class MessageRequest(BaseModel):
    body: str
    from_: str = Field(..., alias='from')

@app.post("/api/process_message")  # Corrected the endpoint path
async def process_message(request: MessageRequest):
    body = request.body
    from_ = request.from_

    # Implement your message processing logic here
    if body == "!ping reply":
        return {"reply": True, "responseMessage": "pong"}
    elif body == "!ping":
        return {"reply": False, "responseMessage": "pong"}
    elif body == "Status":
        return {"reply": False, "responseMessage": "WhatsApp is Online! 🌟"}    
    else:
        raise HTTPException(status_code=204)  # No Content

@app.get("/")
async def root():
    return {"message": "FastAPI WhatsApp is running on port 8000 🌟"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)