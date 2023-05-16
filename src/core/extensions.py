from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.exceptions.handlers import include_exceptions_handlers


# from src.services.scheduler import scheduler
# from src.services.scheduler.daily_planner import (
#     add_idea_view_to_new_employees,
#     plan_councils_starts,
#     remove_role_from_inactive_department,
# )


def include_extensions(app: FastAPI):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    include_exceptions_handlers(app)

    # @app.on_event("startup")
    # async def startup_event():
    #     scheduler.start()
    #     plan_councils_starts.at("03:00").do()
    #     open_award_period.at("03:00").do()
    #     add_idea_view_to_new_employees.at("03:00").do()
    #     remove_role_from_inactive_department.at("04:00").do()
    #     scheduler.do_task(plan_councils_starts)
    #     scheduler.do_task(open_award_period)
    #
    # @app.on_event("shutdown")
    # def shutdown_event():
    #     scheduler.stop()
    #     scheduler.clear()
