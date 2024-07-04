from fastapi import HTTPException
from src.openai_service import callOpenAI
from src.langchain.kb_processor import query_data

# In-memory session store
user_sessions = {}

async def process_message(body: str, from_: str):
    if body == "startchat":
        user_sessions[from_] = True
        return {"reply": True, "responseMessage": "Chatbot session started. How can I assist you?"}
    elif body == "stopchat":
        user_sessions.pop(from_, None)
        return {"reply": True, "responseMessage": "Chatbot session ended."}
    
    if from_ in user_sessions:
        # First try to get response from the knowledge base
        response = await query_data(body)
        if response:
            return {"reply": True, "responseMessage": response}

        # If no response from the knowledge base, fall back to OpenAI
        response = await callOpenAI(body)
        return {"reply": True, "responseMessage": response}
    else:
        # Handle other predefined commands
        if body.startswith("ai "):
            prompt = body[3:]  # Remove 'ai ' from the beginning
            response = await callOpenAI(prompt)
            return {"reply": True, "responseMessage": response}
        elif body.startswith("kb "):
            query = body[3:]  # Remove 'kb ' from the beginning
            response = await query_data(query)
            if response:
                return {"reply": True, "responseMessage": response}
            else:
                return {"reply": True, "responseMessage": "Maaf, saya tidak dapat menemukan informasi yang relevan di basis pengetahuan."}
        elif body == "ping reply":
            return {"reply": True, "responseMessage": "pong"}
        elif body == "ping":
            return {"reply": False, "responseMessage": "pong"}
        elif body == "status":
            return {"reply": False, "responseMessage": "WhatsApp Server Number 1 is Online! 🌟"}
        else:
            raise HTTPException(status_code=204)  # No Content