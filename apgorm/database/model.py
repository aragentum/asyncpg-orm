from apgorm.database.core import BaseModel, String, Integer


class User(BaseModel):
    __tablename__ = "users"

    id = Integer("id")
    username = String("username", 100)
    last_name = String("username", 100)
