from pydantic import BaseModel, EmailStr
from pydantic import field_validator

class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    
    @field_validator("password")
    @classmethod
    def password_length(cls, v:str):
        if len(v) < 8:
            raise ValueError("password must be at least 8 characters")
        return v

class LoginRequest(BaseModel):
    email: EmailStr
    password: str
    
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
    