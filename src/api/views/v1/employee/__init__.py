from .my_ideas import router as my_ideas_router
from .submission import router as submission_router
from .edit_idea import router as edit_idea_router
from .council import router as council_router
from .users_department import router as users_department_router
from .department_ideas import router as department_ideas_router
from .idea_details import router as idea_details_router
from fastapi import APIRouter

router = APIRouter(prefix="/employee")

# /api/v1/idea/employee/my-ideas/*
router.include_router(my_ideas_router)

# /api/v1/idea/employee/submission/*
router.include_router(submission_router)

# /api/v1/idea/employee/edit/*
router.include_router(edit_idea_router)

# /api/v1/idea/employee/council/*
router.include_router(council_router)

# /api/v1/idea/employee/users/*
router.include_router(users_department_router)

# /api/v1/idea/employee/department_ideas/*
router.include_router(department_ideas_router)

# /api/v1/idea/employee/idea_details/*
router.include_router(idea_details_router)
