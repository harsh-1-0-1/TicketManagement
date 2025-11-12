# services/user_service.py
from repository.userRepository import UserRepository
from utils.security import hash_password, get_subject_from_token  # added get_subject_from_token
from fastapi import HTTPException, status
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

    
    def get_user_by_token(self, token: str):
        """
        Decode token to get subject (may be user id or email) and return the user object.
        Raises HTTPException(401) if token invalid or user not found.
        """
        # will raise HTTPException if token invalid/expired
        subject = get_subject_from_token(token)

        user = None

        # if subject looks like an integer, try id lookup
        try:
            uid = int(subject)
        except (TypeError, ValueError):
            uid = None

        if uid is not None and hasattr(self.repo, "get_by_id"):
            user = self.repo.get_by_id(uid)
# fallback: try email lookup
        if user is None and hasattr(self.repo, "get_by_email"):
            user = self.repo.get_by_email(subject)

        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid authentication credentials")

        return user
