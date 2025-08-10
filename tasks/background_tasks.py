import asyncio
import logging
from services.analytics_service import AnalyticsService

logger = logging.getLogger(__name__)
analytics_service = AnalyticsService()

async def update_analytics_periodically(interval_seconds: int = 3600):
    """
    A simple background task that periodically regenerates the analytics data.

    Args:
        interval_seconds: The time to wait between each run (default is 1 hour).
    """
    logger.info("Background analytics refresher has started.")
    while True:
        try:
            logger.info("Running scheduled analytics update...")
            await analytics_service.process_data()
            logger.info(f"Analytics update complete. Next run in {interval_seconds} seconds.")
        except Exception as e:
            logger.error(f"Error in scheduled analytics update: {e}")
        
        # Wait for the specified interval before running again
        await asyncio.sleep(interval_seconds)

def start_background_tasks(app):
    """
    Creates the background task when the FastAPI application starts.
    """
    loop = asyncio.get_event_loop()
    loop.create_task(update_analytics_periodically())
