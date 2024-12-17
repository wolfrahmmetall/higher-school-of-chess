from typing import Any
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy import MetaData, true

class Base(DeclarativeBase):
    __abstract__ = True     
    __name__ :str
    id: Mapped[int] = mapped_column(primary_key=True)

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
        

    