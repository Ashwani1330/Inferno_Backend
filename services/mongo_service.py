from db.mongodb import MongoDB
import logging

logger = logging.getLogger(__name__)

class MongoService:
    def __init__(self):
        """
        Initializes the service with a direct connection to the 'performances' collection.
        """

        self.db = MongoDB.get_db()
        self.performance_collection = self.db["performances"]
        logger.info("MongoService initialized and connected to 'performances' collection.")

    async def insert_performance(self, data: dict) -> bool:
        """
        Inserts a single performance record into the database.
        
        Args:
            data: A dictionary containing the performance data.

        Returns:
            True if insertion in successful, False otherwise.
        """

        try:
            await self.performance_collection.insert_one(data)
            logger.info("Successfully inserted one performance record.")
            return True
        except Exception as e:
            logger.error(f"Error inserting performance data: {e}")
            return False

    async def get_all_performances(self) -> list:
        """
        Retrieves all performance records from the database.

        Returns:
            A list of all performance documents
        """

        try:
            # .to_list(length=1000) will retrieve up to 1000 documents. 
            # This number can be adjusted to the needs.
            performances = await self.performance_collection.find().to_list(length=1000)
            logger.info(f"Successfully retrieved {len(performances)} performance records.")
            return performances
        except Exception as e:
            logger.error(f"Error retrieving performance data: {e}")
            return []
