from dotenv import load_dotenv
import os

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
DATABASE_URL=os.getenv('DATABASE_URL')
GOOGLE_CLIENT_ID=os.getenv('GOOGLE_CLIENT_ID')
GOOGLE_CLIENT_SECRET=os.getenv('GOOGLE_CLIENT_SECRET')
GOOGLE_REDIRECT_URI=os.getenv('GOOGLE_REDIRECT_URI')

MAIL_USERNAME = os.getenv('MAIL_USERNAME')
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  
MAIL_FROM = os.getenv('MAIL_FROM')
MAIL_PORT = os.getenv('MAIL_PORT')
MAIL_SERVER = os.getenv('MAIL_SERVER')
MAIL_TLS = os.getenv('MAIL_TLS')
MAIL_SSL = os.getenv('MAIL_SSL')
USE_CREDENTIALS = os.getenv('USE_CREDENTIALS')
