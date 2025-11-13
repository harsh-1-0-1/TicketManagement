# auth_controller.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from database import get_db
from services.authServices import authService
from repository.userRepository import UserRepository

router = APIRouter()  

def get_auth_service(db: Session = Depends(get_db)):
    repo = UserRepository(db)
    return authService(repo)

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    service: authService = Depends(get_auth_service)
):
    # Swagger sends the email in the "username" field of the form
    token = service.login_user(form_data.username, form_data.password)

    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    # Return the standard OAuth2 response that Swagger expects
    return token
