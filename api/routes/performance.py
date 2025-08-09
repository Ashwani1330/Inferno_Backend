from datetime import datetime
from fastapi import APIRouter, HTTPException
from models.performance import PerformanceInput, PerformanceOutput
from services.mongo_service import MongoService


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
        placeholder_score = 100.0

        performance_data = performance.model_dump()
        performance_data["performanceScore"] = placeholder_score
        performance_data["timestamp"] = datetime.now()

        success = await mongo_service.insert_performance(performance_data)
        if not success:
            raise HTTPException(status_code=500, detail="Failed to save performance data.")

        return {
            "message": "Performance data saved successfully",
            "performanceScore": placeholder_score
        }
    
    except Exception as e:
        # This will catch any errors, including validation errors from Pydantic
        raise HTTPException(status_code=400, detail=str(e))
