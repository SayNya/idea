from sqlalchemy import Column, Integer, MetaData, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

__meta = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
    }
)

Base = declarative_base(metadata=__meta)


class BaseIDModel(Base):
    __abstract__ = True
    __table_args__ = ()

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
