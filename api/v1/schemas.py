from pydantic import BaseModel

class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str

class RegisterResponse(BaseModel):
    message: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RequestData(BaseModel):
    bottoken: str
    chatid: str
    message: str

class DataResponse(BaseModel):
    status: str
    response: str
