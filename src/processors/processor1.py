from fastapi import HTTPException
from src.openai_service import callOpenAI
from src.langchain.kb_processor import query_data

async def process_message(body: str):
    if body.startswith("ai "):
        prompt = body[3:]  # Remove 'ai ' from the beginning
        response = await callOpenAI(prompt)
        return {"reply": True, "responseMessage": response}
    elif body.startswith("kb "):
        query = body[3:]  # Remove 'kb ' from the beginning
        response = await query_data(query)
        return {"reply": True, "responseMessage": response}
    elif body == "ping reply":
        return {"reply": True, "responseMessage": "pong"}
    elif body == "ping":
        return {"reply": False, "responseMessage": "pong"}
    elif body == "status":
        return {"reply": False, "responseMessage": "WhatsApp Server Number 1 is Online! 🌟"}
    else:
        raise HTTPException(status_code=204)  # No Content