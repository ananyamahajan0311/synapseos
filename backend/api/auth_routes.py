from fastapi import APIRouter

from api.schemas import SignupRequest, LoginRequest
from database import SessionLocal
from models import User
from passlib.context import CryptContext
from utils.jwt_handler import create_access_token   # change if your file name is different

router = APIRouter(tags=["Authentication"])

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

@router.post("/signup")
def signup(data: SignupRequest):

    db = SessionLocal()

    existing_user = db.query(User).filter(
        User.email == data.email
    ).first()

    if existing_user:
        db.close()
        return {
            "message": "User already exists"
        }

    hashed_password = pwd_context.hash(
        data.password
    )

    new_user = User(
        username=data.username,
        email=data.email,
        password=hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    db.close()

    return {
        "message": "User created successfully"
    }


@router.post("/login")
def login(data: LoginRequest):

    db = SessionLocal()

    user = db.query(User).filter(
        User.email == data.email
    ).first()

    if not user:
        db.close()
        return {
            "message": "User not found"
        }

    if not pwd_context.verify(
        data.password,
        user.password
    ):
        db.close()
        return {
            "message": "Incorrect password"
        }

    access_token = create_access_token(
        data={
            "sub": user.email
        }
    )

    db.close()

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }