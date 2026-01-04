from pydantic import BaseModel

class ChatRequest(BaseModel):
    user_id: str
    message: str

class ChatResponse(BaseModel):
    is_gold_related: bool
    confidence: float
    response: str
    cta: str | None
    next_action: str

class BuyGoldRequest(BaseModel):
    user_id: str
    amount: float  # INR

class BuyGoldResponse(BaseModel):
    order_id: str
    gold_grams: float
    status: str
    message: str
