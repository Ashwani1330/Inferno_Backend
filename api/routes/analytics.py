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
        data = await analytics_service.get_dashboard_data()
        if not data:
            return HTMLResponse("<h1>No analytics data available yet. Please submit some performance records first.</h1>")

        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "stats": data.get("stats", {}),
                "plots": data.get("plots", {})
            }
        )
    except Exception as e:
        logger.error(f"Error generating dashboard: {e}")
        raise HTTPException(status_code=500, detail="Could not generate dashboard.")

@router.get("/dashboard/refresh")
async def refresh_dashboard_data():
    """
    Manually triggers a regeneration of the dashboard analytics data.
    """
    try:
        success = await analytics_service.process_data()
        if success:
            return {"status": "success", "message": "Dashboard data has been refreshed."}
        else:
            raise HTTPException(status_code=500, detail="Failed to refresh dashboard data.")
    except Exception as e:
        logger.error(f"Error during manual refresh: {e}")
        raise HTTPException(status_code=500, detail=str(e))
