from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
from fastapi import HTTPException

load_dotenv()

client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def callOpenAI(prompt: str) -> str:
    try:
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "Kamu memberikan informasi edukatif terkait beragam topik. Jawablah dalam Bahasa Indonesia tanpa kalimat pembuka atau penjelasan tambahan."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"OpenAI API error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while processing your request.")