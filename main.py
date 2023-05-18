import time

from fastapi import FastAPI, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.views import api_router
from src.core.extensions import include_extensions
from src.orm.async_database import db_session


def create_app():
    app_ = FastAPI()
    app_.include_router(api_router)
    include_extensions(app_)
    return app_


app = create_app()
