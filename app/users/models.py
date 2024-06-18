from sqlalchemy import String, Column, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM

from app.database import Base
from app.users.enums import UserRole


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(ENUM(UserRole), default=UserRole.USER, nullable=False)

    booking = relationship("Bookings", back_populates="user")

    def __str__(self):
        return f"Пользователь {self.email}"
