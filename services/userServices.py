# services/user_service.py
from repository.userRepository import UserRepository
from utils.security import hash_password  # <-- we'll define this in utils/security.py

class UserService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register_user(self, name: str, email: str, password: str, role: str = "user"):
        """
        Register a new user after verifying the email doesn't already exist.
        """
        if self.repo.get_by_email(email):
            raise ValueError("Email already exists.")
        hashed = hash_password(password)
        return self.repo.create_user(name, email, hashed, role)

    def list_users(self, skip: int = 0, limit: int = 100):
        """
        Retrieve all users, paginated.
        """
        users = self.repo.list_users(skip, limit)
        if not users:
            raise ValueError("No users found.")
        return users

    def delete_user(self, user_id: int):
        """
        Delete a user by ID.
        """
        user = self.repo.delete_user(user_id)
        if not user:
            raise ValueError("User not found.")
        return user
