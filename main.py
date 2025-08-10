import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from api.routes.base import router as base_router
from api.routes.performance import router as performance_router
from api.routes.analytics import router as analytics_router
from core.config import API_DESCRIPTION, API_TITLE, API_VERSION
from utils.matplot_config import configure_matplotlib
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from tasks.background_tasks import start_background_tasks


configure_matplotlib()

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

@app.on_event("startup")
async def startup():
    redis_url = os.environ.get("REDIS_URL", "redis://localhost:6379")
    redis = aioredis.from_url(redis_url)
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    # Start background tasks
    start_background_tasks(app)

# Include the base router
app.include_router(base_router)
app.include_router(performance_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")
