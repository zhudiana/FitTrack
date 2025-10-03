from fastapi import APIRouter, HTTPException
from app.core.config import GOOGLE_CLIENT_ID, GOOGLE_REDIRECT_URI
from app.services.google import get_user_infos_from_google_token_url

router = APIRouter()

@router.get("/google/login")
async def login_google():
    # Build the Google login URL
    params = {
        "response_type": "code",
        "client_id": GOOGLE_CLIENT_ID,
        "redirect_uri": GOOGLE_REDIRECT_URI,
        "scope": "openid email profile"
    }

    # Create the query string
    query_string = "&".join(f"{key}={value}" for key, value in params.items())

    # Return the full auth URL
    return {
        "url": f"https://accounts.google.com/o/oauth2/v2/auth?{query_string}"
    }

@router.get("/auth/google/callback")
async def auth_google(code: str = None):
    if not code:
        raise HTTPException(status_code=400, detail="No code provided")

    # Get user info using the code
    result = get_user_infos_from_google_token_url(code)

    if not result['status']:
        raise HTTPException(status_code=400, detail="Couldn't get user info")

    # Return the user info!
    return result['user_infos']
