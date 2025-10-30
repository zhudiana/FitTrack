from fastapi_mail import MessageSchema, FastMail
from jose import jwt
from datetime import datetime, timedelta
from app.core.config import SECRET_KEY
from app.core.email_config import fastmail

async def send_verification_email(email: str, username: str):
    
    token = jwt.encode(
        {
            'email': email,
            'exp': datetime.utcnow() + timedelta(hours=24)
        },
        SECRET_KEY,
        algorithm='HS256'
    )
    
    # Create verification URL
    verify_url = f"http://localhost:8000/auth/verify/{token}"
    
    # Create email body
    html = f"""
        <p>Hi {username},</p>
        <p>Please verify your email by clicking the link below:</p>
        <p><a href="{verify_url}">Verify Email</a></p>
        <p>This link will expire in 24 hours.</p>
    """
    
    # Create message
    message = MessageSchema(
        subject="Verify Your Email",
        recipients=[email],
        body=html,
        subtype="html"
    )
    
    # Send email
    await fastmail.send_message(message)
    return token