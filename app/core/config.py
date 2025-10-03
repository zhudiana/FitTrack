from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
DATABASE_URL=os.getenv('DATABASE_URL')
GOOGLE_CLIENT_ID=os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET=os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI=os.getenv('GOOGLE_REDIRECT_URI')
