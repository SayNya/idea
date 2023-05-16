from fastapi import FastAPI


def create_app():
    app_ = FastAPI()
    # app_.include_router(api_router)
    # include_extensions(app_)
    return app_


app = create_app()
