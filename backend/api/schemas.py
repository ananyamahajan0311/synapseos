from pydantic import BaseModel

class PromptRequest(BaseModel):
    prompt: str


class SendEmailRequest(BaseModel):
    to_email: str
    subject: str
    message: str


class SignupRequest(BaseModel):
    username: str
    email: str
    password: str


class LoginRequest(BaseModel):
    email: str
    password: str