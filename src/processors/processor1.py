from fastapi import HTTPException

def process_message(body: str):
    if body == "!ping reply":
        return {"reply": True, "responseMessage": "pong"}
    elif body == "!ping":
        return {"reply": False, "responseMessage": "pong"}
    elif body == "Status":
        return {"reply": False, "responseMessage": "WhatsApp Server Number 1 is Online! 🌟"}
    else:
        raise HTTPException(status_code=204)  # No Content