from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import create_access_token
from passlib.context import CryptContext
from fastapi import HTTPException, status

from app.schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    return user

def create_user(db: Session, user: UserCreate):
    db_user = User(
        email=user.email,
        hashed_password=get_password_hash(user.password),
        full_name=user.full_name,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_social_user(db: Session, user_data: dict, provider: str):
    social_id = user_data["id"]
    email = user_data["email"]
    full_name = user_data.get("name", "")
    profile_image = user_data.get("picture", "")
    
    user = db.query(User).filter(User.social_id == social_id, User.provider == provider).first()
    if not user:
        user = User(
            email=email,
            full_name=full_name,
            profile_image=profile_image,
            is_social_login=True,
            provider=provider,
            social_id=social_id,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = create_access_token({"sub": user.email})
    return access_token
