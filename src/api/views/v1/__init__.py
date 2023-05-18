from fastapi import APIRouter
from .auth import router as auth_router
from .employee import router as employee_router

v1_router = APIRouter(prefix="/v1")

# /api/v1/auth/*
v1_router.include_router(auth_router)

# /api/v1/employee/*
v1_router.include_router(employee_router)
