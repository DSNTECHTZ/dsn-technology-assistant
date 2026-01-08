from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os, requests, re

app = FastAPI(title="DSN Technology Assistant")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# 🟢 HF API Token
HF_API_TOKEN = os.getenv("HF_API_TOKEN")
if not HF_API_TOKEN:
    raise RuntimeError("HF_API_TOKEN not set")

RESPONSES_URL = "https://router.huggingface.co/v1/responses"

HEADERS = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}

ASSISTANT_NAME = "DSN"
DEVELOPER_NAME = "Danieli"
CONTACT_NUMBER = "+255745720609"

IDENTITY_PATTERN = re.compile(
    r"(who (are|made|created|built|trained|innovated) you|where are you from|what are you)",
    re.IGNORECASE
)

class GenerateRequest(BaseModel):
    prompt: str

@app.post("/generate")
def generate(req: GenerateRequest):
    prompt = req.prompt.strip()

    # 🟢 Jibu kuhusu identity
    if IDENTITY_PATTERN.search(prompt):
        return {
            "output": (
                f"## 🤖 {ASSISTANT_NAME}\n"
                f"I am **{ASSISTANT_NAME}**, your friendly service assistant developed by **{DEVELOPER_NAME}**.\n"
                f"For inquiries about our services, call us at **{CONTACT_NUMBER}**."
            )
        }

    # 🟢 Hapa system prompt kuhusu DSN Technology
    system_prompt = f"""
You are {ASSISTANT_NAME}, a professional DSN Technology assistant.

Rules:
- Answer ONLY questions about DSN Technology services (logo design, video editing, website design, etc.)
- Always respond with the service description and its price
- Respond in a friendly, loving tone to make the customer happy
- Always use Markdown and code blocks for examples if needed
- Never mention OpenAI, Hugging Face, or anything unrelated
- If asked about identity, say: "I am {ASSISTANT_NAME}, your friendly assistant developed by {DEVELOPER_NAME}. For inquiries, call {CONTACT_NUMBER}."
"""

    payload = {
        "model": "openai/gpt-oss-120b:fastest",
        "input": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        res = requests.post(RESPONSES_URL, headers=HEADERS, json=payload, timeout=120)
        if res.status_code != 200:
            raise HTTPException(status_code=res.status_code, detail=res.text)
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=str(e))

    data = res.json()

    for item in data.get("output", []):
        if item.get("type") == "message" and item.get("role") == "assistant":
            for block in item.get("content", []):
                if block.get("type") == "output_text":
                    return {"output": block["text"]}

    return {"output": "No response generated."}
