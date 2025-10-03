from pydantic import BaseModel, EmailStr, PositiveInt, SecretStr


class RegisterUserIn(BaseModel):
    email: EmailStr
    password: SecretStr


class RegisterUserOut(BaseModel):
    id: PositiveInt


class UserOut(BaseModel):
    id: PositiveInt
    email: EmailStr
    role: str


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
