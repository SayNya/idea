from pydantic import Field, PositiveInt, conlist, conset, constr

from src.schemas.base import BaseRequest


class EmployeeSubmitIdeaRequest(BaseRequest):
    title: constr(max_length=300)
    problem_description: constr(max_length=2000)
    solution_description: constr(max_length=2000)
    co_authors_ids: conlist(
        max_items=2, item_type=PositiveInt, unique_items=True
    ) = Field(default_factory=list)
    department_id: PositiveInt
    categories_ids: conset(PositiveInt, min_items=1)
