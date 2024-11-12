from .Base import Base
from sqlalchemy.orm import Mapped

class Password(Base):
    __tablename__ = 'passwords'

    __login: Mapped[str]
    __password: Mapped[str]