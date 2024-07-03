from fastapi import HTTPException

def process_message(body: str):
    # Implement different message processing logic for this number
    if body == "!ping reply":
        return {"reply": True, "responseMessage": "pong from processor 2"}
    elif body == "!ping":
        return {"reply": False, "responseMessage": "pong from processor 2"}
    elif body == "Status":
        return {"reply": False, "responseMessage": "WhatsApp Server is Online! 🌟 (Processor 2)"}
    else:
        raise HTTPException(status_code=204)  # No Content