import pandas as pd
import logging
from services.mongo_service import MongoService
from utils.helpers import parse_age
from datetime import datetime
import os
import json
import io
import base64
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from typing import Optional

logger = logging.getLogger(__name__)

class AnalyticsService:
    def __init__(self):
        self.mongo_service = MongoService()
        self.cache_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "cache", "analytics")
        self.plots_dir = os.path.join(self.cache_dir, "plots")
        self.stats_path = os.path.join(self.cache_dir, "dashboard_stats.json")
        os.makedirs(self.plots_dir, exist_ok=True)

    def optimize_plot(self, fig, title, dpi=80, quality=80, format='webp', max_width=800):
        """Optimizes a matplotlib figure for web display and returns a base64 string."""
        try:
            plt.title(title)
            plt.tight_layout()
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=dpi, bbox_inches='tight')
            buf.seek(0)
            img = Image.open(buf)
            if img.width > max_width:
                ratio = max_width / img.width
                new_height = int(img.height * ratio)
                img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            out_buf = io.BytesIO()
            img.save(out_buf, format=format.upper(), quality=quality)
            out_buf.seek(0)
            img_str = base64.b64encode(out_buf.getvalue()).decode('utf-8')
            mime_type = f'image/{format}'
            plt.close(fig)
            return {
                'base64': f'data:{mime_type};base64,{img_str}',
                'filename': f"{title.lower().replace(' ', '_')}.{format}"
            }
        except Exception as e:
            logger.error(f"Error optimizing plot '{title}': {e}")
            plt.close(fig)
            return {'base64': '', 'filename': 'error.png'}

    async def process_data(self) -> bool:
        """
        The main data processing and plot generation "worker" function.
        It fetches all data, generates stats and plots, and caches them to a JSON file.
        """
        try:
            performances = await self.mongo_service.get_all_performances()
            if not performances:
                logger.warning("No performance data for analytics.")
                # Create an empty cache file if no data exists
                with open(self.stats_path, 'w') as f:
                    json.dump({'stats': {}, 'plots': {}}, f, indent=4)
                return True

            df = pd.DataFrame(performances)
            df['numeric_age'] = df['age'].apply(lambda x: parse_age(str(x)))
            df['age_group'] = pd.cut(df['numeric_age'],
                                     bins=[0, 18, 30, 45, 60, 100],
                                     labels=['Under 18', '18-30', '31-45', '46-60', 'Over 60'],
                                     include_lowest=True)

            stats = {
                'participant_count': len(df),
                'avg_score': round(df['performanceScore'].mean(), 2),
                'avg_evacuation_time': round(df[['timeToFindExtinguisher', 'timeToExtinguishFire', 'timeToTriggerAlarm', 'timeToFindExit']].sum(axis=1).mean(), 2),
                'success_rate': round((df['performanceScore'] > 0).mean() * 100, 2),
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }

            plots = {}

            # Plot 1: Performance Score Distribution
            fig = plt.figure(figsize=(8, 5))
            sns.histplot(x=df['performanceScore'], kde=True, bins=15, color='steelblue')
            plots['performance_distribution'] = self.optimize_plot(fig, 'Distribution of Performance Scores')

            # Plot 2: Performance by Age Group
            fig = plt.figure(figsize=(10, 6))
            sns.boxplot(x='age_group', y='performanceScore', data=df, palette='viridis', order=['Under 18', '18-30', '31-45', '46-60', 'Over 60'], hue='age_group', legend=False)
            plt.xticks(rotation=45)
            plots['performance_by_age'] = self.optimize_plot(fig, 'Performance Score by Age Group')
            
            # Plot 3: Performance by Difficulty
            if 'difficulty' in df.columns:
                fig = plt.figure(figsize=(10, 6))
                sns.barplot(x='difficulty', y='performanceScore', data=df, palette='YlOrRd', errorbar='sd', hue='difficulty', legend=False)
                plots['performance_by_difficulty'] = self.optimize_plot(fig, 'Performance by Difficulty Level')

            dashboard_data = {'stats': stats, 'plots': plots}
            with open(self.stats_path, 'w') as f:
                json.dump(dashboard_data, f, indent=4)

            logger.info("Successfully processed and cached analytics stats and plots.")
            return True

        except Exception as e:
            logger.error(f"Error processing analytics data: {e}", exc_info=True)
            return False

    async def get_dashboard_data(self) -> Optional[dict]:
        """
        Retrieves dashboard data from the JSON cache. If it doesn't exist,
        it triggers a regeneration.
        """
        try:
            if not os.path.exists(self.stats_path):
                logger.info("Cache file not found. Regenerating dashboard data...")
                await self.process_data()

            if os.path.exists(self.stats_path):
                with open(self.stats_path, 'r') as f:
                    return json.load(f)
            return None
        except Exception as e:
            logger.error(f"Error retrieving dashboard data: {e}")
            return None
