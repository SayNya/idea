import functools

from src.orm.async_database import db_session, async_session


def session(*, commit: bool = False):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            async with async_session() as session_:
                db_session.set(session_)
                response = await func(*args, **kwargs)
                if commit:
                    await db_session.get().commit()
            return response

        return wrapper

    return decorator
