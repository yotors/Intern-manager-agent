import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Google API Configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', '')
GOOGLE_FORM_ID = os.getenv('GOOGLE_FORM_ID', '')
GOOGLE_CREDENTIALS_PATH = os.getenv('GOOGLE_CREDENTIALS_PATH', 'credentials.json')

# Email Configuration
SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
SMTP_PORT = int(os.getenv('SMTP_PORT', '587'))
EMAIL_USERNAME = os.getenv('EMAIL_USERNAME', '')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')

# GitHub Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN', '')

# Application Configuration
MAX_INTERNS = int(os.getenv('MAX_INTERNS', '10')) 