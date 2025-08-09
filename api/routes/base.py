from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    """A simple greeting to confirm the API is running."""
    return {"message": "Welcome to the Inferno VR Fire-Safety Training API"}
