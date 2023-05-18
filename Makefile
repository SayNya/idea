debug:
	uvicorn main:app --reload
generate:
	alembic revision --autogenerate
migrate:
	alembic upgrade head
downgrade:
	alembic downgrade -1