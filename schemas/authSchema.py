# app/schemas/auth.py
from pydantic import BaseModel , EmailStr
from fastapi import Form

class  loginRequest(BaseModel):
    email:EmailStr
    password: str


class OAuth2PasswordRequestFormEmail:
    def __init__(self, email: str = Form(...), password: str = Form(...)):
        self.email = email
        self.password = password
