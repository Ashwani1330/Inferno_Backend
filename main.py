from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.routes.base import router as base_router
from api.routes.performance import router as performance_router
from api.routes.analytics import router as analytics_router
from core.config import API_DESCRIPTION, API_TITLE, API_VERSION

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

app.mount("/static", StaticFiles(directory="static"), name="static")

# Include the base router
app.include_router(base_router)
app.include_router(performance_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")
