from .council import router as council_router
from fastapi import APIRouter

router = APIRouter(prefix="/employee")

# /api/v1/idea/my-ideas/*
router.include_router(council_router)

# /api/v1/idea/submission/*
router.include_router(submission_router)

# /api/v1/idea/edit/*
router.include_router(edit_idea_router)
