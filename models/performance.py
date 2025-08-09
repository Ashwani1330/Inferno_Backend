from pydantic import BaseModel, Field
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
