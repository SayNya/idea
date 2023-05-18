from fastapi import FastAPI

from src.api.views import api_router
from src.core.extensions import include_extensions


def create_app():
    app_ = FastAPI()
    app_.include_router(api_router)
    include_extensions(app_)
    return app_


app = create_app()
