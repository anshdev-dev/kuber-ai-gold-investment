from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import RedirectResponse

from config import API_KEY
from schemas import (
    ChatRequest,
    ChatResponse,
    BuyGoldRequest,
    BuyGoldResponse
)
from llm import run_llm
from db import init_db, create_user_if_not_exists, create_gold_order

app = FastAPI(
    title="Kuber AI – Gold Investment Demo",
    description="AI-powered gold investment assistant emulating Simplify Money's Kuber AI workflow.",
    version="1.0.0"
)

# -------------------------------
# Startup: Initialize Database
# -------------------------------
@app.on_event("startup")
def on_startup():
    init_db()


# -------------------------------
# Root Redirect (Reviewer Convenience)
# -------------------------------
@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse(url="/docs")


# -------------------------------
# API Key Verification
# -------------------------------
def verify_api_key(x_api_key: str = Header(...)):
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API Key")


# -------------------------------
# Health Check
# -------------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# -------------------------------
# Chat API (AI + Gold Intent Detection)
# -------------------------------
@app.post("/chat", response_model=ChatResponse)
def chat(payload: ChatRequest, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)

    # Normalize input slightly (safe, optional hygiene)
    user_message = payload.message.strip()

    # LLM handles intent + response
    return run_llm(user_message)


# -------------------------------
# Buy Gold API (Mock Transaction)
# -------------------------------
@app.post("/buy-gold", response_model=BuyGoldResponse)
def buy_gold(payload: BuyGoldRequest, x_api_key: str = Header(...)):
    verify_api_key(x_api_key)

    # Ensure user exists
    create_user_if_not_exists(payload.user_id)

    # Create gold order
    order_id, gold_grams = create_gold_order(
        payload.user_id,
        payload.amount
    )

    return BuyGoldResponse(
        order_id=order_id,
        user_id=payload.user_id,
        gold_grams=gold_grams,
        status="SUCCESS",
        message="Digital gold purchased successfully."
    )


# -------------------------------
# Local Run (Optional)
# -------------------------------
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
