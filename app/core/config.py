from dotenv import load_dotenv
import os
from app.db.database import DATABASE_URL

load_dotenv()

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
DATABASE_URL=os.getenv('DATABASE_URL')

