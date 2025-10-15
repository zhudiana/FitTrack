from fastapi import APIRouter, HTTPException
from app.core.config import GOOGLE_CLIENT_ID, GOOGLE_REDIRECT_URI
from app.services.google import get_user_infos_from_google_token_url
from app.dependencies import db_dependency
from app.db.models import Users

router = APIRouter()

@router.get("/google/login")
async def login_google():
    params = {
        "response_type": "code",
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "scope": "openid email profile",
        "prompt": "consent",
        "access_type": "offline"
    }

    # Create the query string
    query_string = "&".join(f"{key}={value}" for key, value in params.items())

    
    return {
        "url": f"https://accounts.google.com/o/oauth2/v2/auth?{query_string}"
    }

@router.get("/auth/google/callback")
async def auth_google(db: db_dependency, code: str = None):
    if not code:
        raise HTTPException(status_code=400, detail="No code provided")

    result = get_user_infos_from_google_token_url(code)

    if not result['status']:
        raise HTTPException(status_code=400, detail="Couldn't get user info")

    user_info = result["user_infos"]

    existing_user = db.query(Users).filter(Users.email == user_info['email']).first()

    if existing_user:
        user = existing_user
    else:
        new_user = Users(
            username=user_info['email'].split('@')[0],  # or generate unique username
            email=user_info['email'],
            verified_email=user_info['verified_email'],
            is_oauth=True,
            oauth_provider="Google"
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        user = new_user

        return {"message": "Login successful", "user": user.email}