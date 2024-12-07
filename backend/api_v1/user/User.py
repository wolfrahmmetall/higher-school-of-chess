
from sqlalchemy.orm import Mapped, mapped_column
from dbpackage.Base import Base

# to be used once migrations are done
# class Auth(Base):
#     login: Mapped[str]
#     password: Mapped[bytes]

class User(Base):
    """
    Базовый класс пользователя -- хранит его логин и почту. 
    Логин используется как User ID во всех БД
    """
    #equivalent to UID. To be used that way 
    # login : Mapped[str] = mapped_column(ForeignKey('auth.login', ondelete=CASCADE)) to be this way once migrations are done
    login : Mapped[str]
    # TODO: update the key to be an uuid, login is to be used as a mean to get it
    password: Mapped[bytes] # get rid of this as soon as possible
    email : Mapped[str]
    elo_score : Mapped[float| None] = mapped_column(nullable=True)

