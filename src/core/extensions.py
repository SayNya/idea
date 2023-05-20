from fastapi import FastAPI

from src.api.middlewares import include_cors_middleware
from src.exceptions.handlers import include_exceptions_handlers


from src.services.scheduler import scheduler
from src.services.scheduler.daily_planner import (
    plan_councils_starts,
    remove_role_from_inactive_department,
)


def include_extensions(app: FastAPI):
    include_cors_middleware(app)
    include_exceptions_handlers(app)

    @app.on_event("startup")
    async def startup_event():
        scheduler.start()
        plan_councils_starts.at("03:00").do()
        remove_role_from_inactive_department.at("04:00").do()
        scheduler.do_task(plan_councils_starts)

    @app.on_event("shutdown")
    def shutdown_event():
        scheduler.stop()
        scheduler.clear()
