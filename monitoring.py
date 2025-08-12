from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import datetime, timedelta
import time
from app.utils.database import db
from app.config import settings

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request):
    # Statistiques globales
    total_requests = await db.api_logs.count_documents({})
    last_hour = datetime.utcnow() - timedelta(hours=1)
    recent_requests = await db.api_logs.count_documents({
        "timestamp": {"$gte": last_hour}
    })
    
    # Top utilisateurs
    pipeline = [
        {"$group": {"_id": "$user_id", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 5}
    ]
    top_users = await db.api_logs.aggregate(pipeline).to_list(None)
    
    # Modèles les plus utilisés
    model_pipeline = [
        {"$group": {"_id": "$model", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    top_models = await db.api_logs.aggregate(model_pipeline).to_list(None)
    
    return templates.TemplateResponse("index.html", {
        "request": request,
        "total_requests": total_requests,
        "recent_requests": recent_requests,
        "top_users": top_users,
        "top_models": top_models,
        "uptime": get_uptime()
    })

@router.get("/metrics", response_class=HTMLResponse)
async def metrics(request: Request):
    # Données pour les graphiques
    time_points = []
    request_counts = []
    
    now = datetime.utcnow()
    for i in range(24):
        start = now - timedelta(hours=i+1)
        end = now - timedelta(hours=i)
        count = await db.api_logs.count_documents({
            "timestamp": {"$gte": start, "$lt": end}
        })
        time_points.append(end.strftime("%H:%M"))
        request_counts.append(count)
    
    return templates.TemplateResponse("metrics.html", {
        "request": request,
        "time_points": reversed(time_points),
        "request_counts": reversed(request_counts)
    })

def get_uptime():
    return time.time() - settings.START_TIME
