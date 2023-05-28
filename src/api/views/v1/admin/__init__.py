from .council import router as council_router
from .set_responsible import router as set_responsible_router
from .voting_employees import router as voting_employees_router
from fastapi import APIRouter

router = APIRouter(prefix="/admin")

# /api/v1/idea/admin/council/*
router.include_router(council_router)

# /api/v1/idea/admin/set_responsible/*
router.include_router(set_responsible_router)

# /api/v1/idea/admin/voting_employees/*
router.include_router(voting_employees_router)
