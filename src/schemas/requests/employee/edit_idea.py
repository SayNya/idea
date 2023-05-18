from pydantic import Field, PositiveInt, conset, constr

from src.schemas.base import BaseRequest


class EditIdeaRequest(BaseRequest):
    title: constr(max_length=300)
    problem_description: constr(max_length=2000)
    solution_description: constr(max_length=2000)
    co_authors_ids: conset(max_items=2, item_type=PositiveInt) = Field(
        default_factory=set
    )
    department_id: PositiveInt
    categories_ids: conset(PositiveInt, min_items=1)
