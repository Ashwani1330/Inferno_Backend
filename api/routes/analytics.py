from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.analytics_service import AnalyticsService
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"]
)

# Initialize services and templates
analytics_service = AnalyticsService()
templates = Jinja2Templates(directory="templates")

@router.get("/dashboard", response_class=HTMLResponse)
async def get_analytics_dashboard(request: Request):
    """
    Serves the main analytics dashboard.
    """
    try:
        data = await analytics_service.process_data_and_generate_stats()
        if not data or 'stats' not in data:
            return HTMLResponse("<h1>No analytics data available yet. Please submit some performance records first.</h1>")

        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "stats": data.get("stats", {})
            }
        )
    except Exception as e:
        logger.error(f"Error generating dashboard: {e}")
        raise HTTPException(status_code=500, detail="Could not generate dashboard.")
