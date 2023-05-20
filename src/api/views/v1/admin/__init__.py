from .council import router as council_router
from .accept_idea import router as accept_idea_router
from fastapi import APIRouter

router = APIRouter(prefix="/admin")

# /api/v1/idea/my-ideas/*
router.include_router(council_router)

# /api/v1/idea/admin/accept_idea/*
router.include_router(accept_idea_router)
