# fastapi-social-login

uvicorn app.main:app --reload --port 30099

# .env

# Secret key for JWT

SECRET_KEY="..."

# Database configuration

DATABASE_URL="postgresql://user_id:pwd@db_address/db_name"

# OAuth2 Configuration for Google

GOOGLE_CLIENT_ID="..."
GOOGLE_CLIENT_SECRET="..."
REDIRECT_URI_GOOGLE="http://localhost:30099/auth/google/callback"

# OAuth2 Configuration for Kakao

KAKAO_CLIENT_ID="..."
