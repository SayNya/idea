from .my_ideas import router as my_ideas_router
from fastapi import APIRouter

router = APIRouter(prefix="/employee")

# /api/v1/idea/my-ideas/*
router.include_router(my_ideas_router)
