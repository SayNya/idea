from fastapi import APIRouter
from .auth import router as auth_router

v1_router = APIRouter(prefix="/v1")

# /api/v1/auth/*
v1_router.include_router(auth_router)
