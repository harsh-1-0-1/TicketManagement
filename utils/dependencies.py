from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from services.userServices import UserService
from database import get_db
from repository.userRepository import UserRepository



oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")  # modify tokenUrl as needed

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):

    user_service = UserService(repo=UserRepository(db))
    
    user = user_service.get_user_by_token(token)  # You implement this method to decode and validate JWT, then fetch user
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    return user
