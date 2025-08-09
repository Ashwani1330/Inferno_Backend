import pandas as pd
import logging
from services.mongo_service import MongoService
from utils.helpers import parse_age
from datetime import datetime
import os
import json

logger = logging.getLogger(__name__)

class AnalyticsService:
    def __init__(self):
        self.mongo_service = MongoService()
        # Define a cache directory for our generated stats and plots
        self.cache_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache", "analytics")
        self.plots_dir = os.path.join(self.cache_dir, "plots")
        self.stats_path = os.path.join(self.cache_dir, "dashboard_stats.json")

        # Ensure cache directories exist 
        os.makedirs(self.plots_dir, exist_ok=True)

    async def process_data_and_generate_stats(self) -> dict:
        """
        Fetches all performance data, processes it, and generates key statistics.
        """
        try:
            performances = await self.mongo_service.get_all_performances()
            if not performances:
                    logger.warning("No performance data available for analysis.")
                    return {}
            
            df = pd.DataFrame(performances)

            # --- Data Cleaning and Feature Engineering ---
            df['numeric_age'] = df['age'].apply(lambda x: parse_age(str(x)))

            # --- Calculate Key Metrics ---
            stats = {
                    'participant_count': len(df),
                    'avg_score':  round(df['performanceScore'].mean(), 2),
                    'avg_evacuation_time': round(df[['timeToFindExtinguisher', 'timeToExtinguishFire', 'timeToTriggerAlarm', 'timeToFindExit']].sum(axis=1).mean(), 2),
                    'success_rate': round((df['performanceScore'] > 0).mean() * 100, 2),
                    'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }

            # Cache the stats to a JSON file
            with open(self.stats_path, 'w') as f:
                json.dump({'stats': stats}, f)

            logger.info("Successfully processed and cached analytics stats.")
            return {'stats': stats}
        
        except Exception as e:
            logger.error(f"Error processing analytics data: {e}")
            return {}
