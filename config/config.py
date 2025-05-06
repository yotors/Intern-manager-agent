import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Forms Configuration
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
GOOGLE_FORM_ID = os.getenv('GOOGLE_FORM_ID')

# GitHub Configuration
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Email Configuration
EMAIL_USERNAME = os.getenv('EMAIL_USERNAME')
EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD')
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587

# Application Settings
MAX_INTERNS = 10  # Maximum number of interns to select
MIN_REPOS = 3     # Minimum number of repositories required
MIN_CONTRIBUTIONS = 50  # Minimum number of contributions required

# Calendar Settings
EXAM_DURATION_HOURS = 2
EXAM_BUFFER_DAYS = 7  # Minimum days between exams 