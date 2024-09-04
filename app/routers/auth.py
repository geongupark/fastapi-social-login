from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import create_access_token
from app.db.session import get_db
from app.schemas.user import UserCreate, Token
from app.services.auth_service import authenticate_user, create_user, authenticate_social_user
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import requests

router = APIRouter()

@router.post("/signup", response_model=Token)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = create_user(db, user)
    access_token = create_access_token(data={"sub": db_user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    access_token = create_access_token(data={"sub": user.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/auth/google")
def google_login():
    google_auth_url = (
        f"https://accounts.google.com/o/oauth2/v2/auth?"
        f"client_id={settings.GOOGLE_CLIENT_ID}&"
        f"response_type=code&"
        f"redirect_uri={settings.REDIRECT_URI_GOOGLE}&"
        f"scope=openid%20email%20profile"
    )
    return {"auth_url": google_auth_url}

@router.get("/auth/google/callback")
def google_callback(code: str, db: Session = Depends(get_db)):
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.REDIRECT_URI_GOOGLE,
        "grant_type": "authorization_code",
    }

    token_response = requests.post(token_url, data=token_data)
    token_response_json = token_response.json()
    access_token = token_response_json.get("access_token")

    if not access_token:
        raise HTTPException(status_code=400, detail="Failed to retrieve access token")

    user_info_response = requests.get(
        "https://www.googleapis.com/oauth2/v1/userinfo",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    user_info = user_info_response.json()

    jwt_token = authenticate_social_user(db, user_info, provider="google")
    print(jwt_token)
    return RedirectResponse(url=f"http://localhost:3000/home?token={jwt_token}")
