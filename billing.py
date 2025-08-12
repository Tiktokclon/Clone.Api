import time
from datetime import datetime, timedelta
from fastapi import HTTPException
from pydantic import BaseModel
from typing import Dict, Optional
from app.utils.database import db
from app.config import settings

class BillingPlan(BaseModel):
    id: str
    name: str
    rate_per_token: float
    monthly_fee: float
    features: Dict[str, bool]

class UserSubscription(BaseModel):
    user_id: str
    plan_id: str
    tokens_used: int
    last_payment: datetime
    next_billing: datetime
    payment_method: Optional[str]
    active: bool

# Plans disponibles
PLANS = {
    "free": BillingPlan(
        id="free",
        name="Free Tier",
        rate_per_token=0.01,  # $0.01 per 1k tokens
        monthly_fee=0,
        features={
            "no_filters": True,
            "max_tokens": 10000,
            "priority": False
        }
    ),
    "pro": BillingPlan(
        id="pro",
        name="Pro Plan",
        rate_per_token=0.005,
        monthly_fee=20,
        features={
            "no_filters": True,
            "max_tokens": 100000,
            "priority": True
        }
    ),
    "enterprise": BillingPlan(
        id="enterprise",
        name="Enterprise",
        rate_per_token=0.002,
        monthly_fee=500,
        features={
            "no_filters": True,
            "max_tokens": float('inf'),
            "priority": True,
            "dedicated": True
        }
    )
}

async def check_usage(user_id: str, tokens: int) -> bool:
    """Vérifie si l'utilisateur a assez de crédit"""
    sub = await db.user_subs.find_one({"user_id": user_id})
    if not sub or not sub.get("active"):
        raise HTTPException(status_code=403, detail="Subscription required")
    
    plan = PLANS.get(sub["plan_id"])
    if not plan:
        raise HTTPException(status_code=403, detail="Invalid plan")
    
    # Pour les plans avec limite de tokens
    if plan.features["max_tokens"] != float('inf'):
        if sub["tokens_used"] + tokens > plan.features["max_tokens"]:
            raise HTTPException(status_code=429, detail="Token limit exceeded")
    
    return True

async def record_usage(user_id: str, tokens: int):
    """Enregistre l'utilisation et facture en temps réel"""
    await db.user_subs.update_one(
        {"user_id": user_id},
        {"$inc": {"tokens_used": tokens}},
        upsert=True
    )
    
    # Facturation immédiate pour les pay-as-you-go
    sub = await db.user_subs.find_one({"user_id": user_id})
    plan = PLANS.get(sub["plan_id"])
    if plan and plan.rate_per_token > 0:
        charge = tokens * plan.rate_per_token / 1000
        await db.billing_records.insert_one({
            "user_id": user_id,
            "amount": charge,
            "tokens": tokens,
            "timestamp": datetime.utcnow(),
            "description": "API Usage"
        })

async def create_subscription(user_id: str, plan_id: str, payment_method: str = None):
    """Crée un nouvel abonnement"""
    if plan_id not in PLANS:
        raise HTTPException(status_code=400, detail="Invalid plan ID")
    
    now = datetime.utcnow()
    next_billing = now + timedelta(days=30)
    
    await db.user_subs.insert_one({
        "user_id": user_id,
        "plan_id": plan_id,
        "tokens_used": 0,
        "last_payment": now,
        "next_billing": next_billing,
        "payment_method": payment_method,
        "active": True
    })
    
    # Facture le frais mensuel si applicable
    plan = PLANS[plan_id]
    if plan.monthly_fee > 0:
        await db.billing_records.insert_one({
            "user_id": user_id,
            "amount": plan.monthly_fee,
            "tokens": 0,
            "timestamp": now,
            "description": "Monthly subscription"
        })
