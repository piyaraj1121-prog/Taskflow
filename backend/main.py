from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

from .database import Base, engine
from . import models
from .routes import router


app = FastAPI(
    title="TaskFlow API",
    description="Task and Project Management API",
    version="1.0.0"
)


# Include API routes
app.include_router(router)


# Create database tables
Base.metadata.create_all(bind=engine)


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5500",
        "http://127.0.0.1:5500",
    ],
    allow_credentials=True,
    allow_methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
    ],
    allow_headers=[
        "Content-Type",
        "Authorization",
    ],
)


# Request logging middleware
@app.middleware("http")
async def log_requests(request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    process_time = (time.perf_counter() - start_time) * 1000

    print(
        f"{request.method} {request.url.path} "
        f"- {process_time:.2f} ms"
    )

    return response


# Root endpoint
@app.get("/")
def root():
    return {
        "message": "TaskFlow API is running"
    }


# Health check
@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }