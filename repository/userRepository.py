# repositories/user_repository.py
from sqlalchemy.orm import Session
from models.userModel import User   

class UserRepository:
    """
    Handles all direct database operations related to the User model.
    """

    def __init__(self, db: Session):
        self.db = db

    def create_user(self, name: str, email: str, hashed_password: str, role: str = "user"):
        """
        Create and persist a new user in the database.
        """
        user = User(
            name=name,
            email=email,
            hashed_password=hashed_password,
            role=role
        )
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def list_users(self, skip: int = 0, limit: int = 100):
        """
        Return a paginated list of users.
        """
        return self.db.query(User).offset(skip).limit(limit).all()

    def delete_user(self, user_id: int):
        """
        Delete a user by ID.
        """
        user = self.get_by_id(user_id)
        if user:
            self.db.delete(user)
            self.db.commit()
        return user
    def get_by_email(self, email: str):
        """
        Retrieve a user by their email.
        """
        return self.db.query(User).filter(User.email == email).first()
    def get_by_id(self, user_id: int):
        """ 
        retrieve a user by their ID.
        """
        return self.db.query(User).filter(User.id == user_id).first()