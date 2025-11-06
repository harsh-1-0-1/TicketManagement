from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from repository.userRepository import UserRepository
from services.userServices import UserService
from schemas.userSchema import UserCreate, UserOut, UserLogin  # import exactly as defined


router = APIRouter()

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    repo = UserRepository(db)
    return UserService(repo)

@router.post("/create", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_in:UserCreate, service: UserService = Depends(get_user_service)):
    try:
        return service.register_user(**user_in.dict())
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
@router.get("/list", response_model=list[UserOut])
def list_users(skip: int = 0, limit: int = 100, service: UserService = Depends(get_user_service)):
    try:
        users = service.list_users(skip, limit)
        return users
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))