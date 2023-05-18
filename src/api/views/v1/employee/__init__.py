from .my_ideas import router as my_ideas_router
from .submission import router as submission_router
from .edit_idea import router as edit_idea_router
from fastapi import APIRouter

router = APIRouter(prefix="/employee")

# /api/v1/idea/my-ideas/*
router.include_router(my_ideas_router)

# /api/v1/idea/submission/*
router.include_router(submission_router)

# /api/v1/idea/edit/*
router.include_router(edit_idea_router)
