from src.orm.models import DepartmentModel
from src.orm.repositories.base import BaseRepository


class DepartmentRepository(BaseRepository):
    Model = DepartmentModel
