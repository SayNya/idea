from enum import Enum


class SystemRoleCodeEnum(str, Enum):
    EMPLOYEE = "employee"
    ADMIN = "admin"
    OWNER = "owner"
