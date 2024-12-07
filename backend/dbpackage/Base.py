from typing import Any
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, declared_attr
from sqlalchemy import MetaData

class Base(DeclarativeBase):
    __abstract__ = True     
    id: Any
    __name__ :str

    @declared_attr.directive
    def __tablename__(cls) -> str:
        return cls.__name__.lower()
        
    id: Mapped[int] = mapped_column(primary_key=True)

    