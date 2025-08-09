from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException
from models.performance import PerformanceInput, PerformanceOutput, PerformanceRecord
from services.mongo_service import MongoService
from utils.helpers import parse_age
from utils.score_calculator import calculate_evacuation_efficiency_score


router = APIRouter(
    prefix="/performance",
    tags=["Performance"]
)

# Initialize services
mongo_service = MongoService()

@router.post("", response_model=PerformanceOutput)
async def create_performance_record(performance: PerformanceInput):
    """
    Receives performance data from a VR session, calculates the score,
    and stores it in the database
    """

    try:
        # 1. Parse the age string into a number
        numeric_age = parse_age(performance.age)

        # 2. Group the time metrics into a dictionary
        times = {
            "timeToFindExtinguisher": performance.timeToFindExtinguisher,
            "timeToExtinguishFire": performance.timeToExtinguishFire,
            "timeToTriggerAlarm": performance.timeToTriggerAlarm,
            "timeToFindExit": performance.timeToFindExit
        }

        # 3. Calculate the actual performance score
        performance_score = calculate_evacuation_efficiency_score(numeric_age, times)

        # 4. Prepare data for database insertion
        performance_data = performance.model_dump()
        performance_data["performanceScore"] = performance_score
        performance_data["timestamp"] = datetime.now()

        # 5. Insert into the database
        success = await mongo_service.insert_performance(performance_data)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to save performance data.")

        return {
            "message": "Performance data saved successfully",
            "performanceScore": performance_score
        }
    
    except Exception as e:
        # This will catch any errors, including validation errors from Pydantic
        raise HTTPException(status_code=400, detail=str(e))

@router.get("", response_model=List[PerformanceRecord])
async def get_all_performance_records():
    """
    Retrieves all the performance records stored in the database.
    """

    try:
        performances = await mongo_service.get_all_performances()
        if not performances:
            return []
        
        # Convert MongoDB's ObjectId to a string for each document
        for p in performances:
            p["_id"] = str(p["_id"])

        return performances
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
