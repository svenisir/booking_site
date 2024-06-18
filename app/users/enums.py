import enum


class UserRole(enum.Enum):
    ADMIN = "admin"
    MODERATOR = "moderator"
    USER = "user"
