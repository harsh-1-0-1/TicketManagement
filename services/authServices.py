from utils.security import verify_password
import utils.security as jwt_utils
from repository.userRepository import UserRepository

class authService:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def login_user(self, email: str, password: str):
        user = self.repo.get_by_email(email)
    
        if not user or not verify_password(password, user.hashed_password):
           return None
    
        access_token = jwt_utils.create_access_token(data={"sub": str(user.id), "role": user.role})
        return {"access_token": access_token, "token_type": "bearer"}
