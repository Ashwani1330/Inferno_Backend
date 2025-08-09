from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field
from typing import Optional 

# Performance data models for the Inferno VR application
# These models handle input from VR sessions and output responses

class PerformanceInput(BaseModel):
    """
    Pydantic model for validating incoming performance data from VR sessions.
    """

    email: Optional[str] = None
    age: str
    sceneType: str
    difficulty: str
    timeToFindExtinguisher: float
    timeToExtinguishFire: float
    timeToTriggerAlarm: float
    timeToFindExit: float

class PerformanceOutput(BaseModel):
    """
    Pydantic model for the response after submitting performance data. 
    """

    message: str
    performanceScore: float

class PerformanceRecord(BaseModel):
    """
    Pydantic model representing a full performance record from the database.
    """

    # We use aliases to map MongoDB's '_id' to a Pydantic 'id' field.
    id: str = Field(..., alias="_id")
    email: Optional[str] = None
    age: str
    sceneType: str
    difficulty: str
    timeToFindExtinguisher: float
    timeToExtinguishFire: float
    timeToTriggerAlarm: float
    timeToFindExit: float
    performanceScore: float
    timestamp: datetime
    
    # This configuration allows Pydantic to correctly handle MongoDB's ObjectId
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={datetime: lambda dt: dt.isoformat()}
    )
