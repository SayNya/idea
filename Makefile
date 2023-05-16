debug:
	uvicorn main:app --reload
generate-migrations:
	alembic revision --autogenerate
migrate:
	alembic upgrade head