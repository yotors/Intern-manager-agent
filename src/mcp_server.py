from typing import Any
import httpx
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.email.email_handler import EmailHandler
from forms.google_forms_handler import GoogleFormsHandler
from mcp.server.fastmcp import FastMCP
from config import config
from src.calendar.exam_scheduler import ExamScheduler
from src.github.github_analyzer import GitHubAnalyzer
from src.ranking.applicant_ranker import ApplicantRanker

API_KEY = config.GOOGLE_API_KEY
FORM_ID = config.GOOGLE_FORM_ID
GITHUB_TOKEN = config.GITHUB_TOKEN
STMP_SERVER = config.SMTP_SERVER
STMP_PORT = config.SMTP_PORT
USERNAME = config.EMAIL_USERNAME
PASSWORD = config.EMAIL_PASSWORD
max_interns = config.MAX_INTERNS

mcp = FastMCP(title="MCP Server")
form = GoogleFormsHandler(api_key=API_KEY, form_id=FORM_ID)
email = EmailHandler(USERNAME, PASSWORD, STMP_SERVER, STMP_PORT)
calendar = ExamScheduler()
github = GitHubAnalyzer(token=GITHUB_TOKEN)
ranker = ApplicantRanker(max_interns)
SCOPES = "https://www.googleapis.com/auth/forms.body.readonly"
DISCOVERY_DOC = "https://forms.googleapis.com/$discovery/rest?version=v1"


@mcp.tool()
def submitions():
    """
    Retrieve all submissions from the Google Form.

    Returns:
        list: A list of submission records, each containing applicant details and responses.
    """
    return form.get_submissions()

@mcp.tool()
def send_email(applicants:list):
    """
    Send a confirmation email to applicants.

    Parameters:
        applicants (list): List of applicants' information. This is a list of dictionary containing applicants details such as name and email.
            Example: [{"name": "John Doe", "email": "applicant@example.com"}, {"name": "John Doe", "email": "applicant@example.com"}]

    Returns:
        Bool
    """
    return email.send_confirmation_email(applicants)

@mcp.tool()
def send_exam_schedule(applicants:list, exam_date:str):
    """
    Send an exam schedule to an applicant.

    Parameters:
        applicants (list): The applicants' information list of dict with details.
            Example: [{"name": "Jane Doe", "email": "applicant@example.com"}, {"name": "John Doe", "email": "applicant@example.com"}]
        exam_date (str): The date and time of the exam in ISO format.

    Returns:
        None
    """
    return email.send_exam_schedule(applicants, exam_date)

@mcp.tool()
def check_confirmation(applicants_emails:list):
    """
    Check if applicant had confirmed their participation via email.

    Parameters:
        applicants_emails (list): The list of email of addresses of the applicants.
            Example: ["applicant@example.com", "applicant1@example.com"]

    Returns:
        bool: True if confirmed, False otherwise.
    """ 
    return email.check_confirmation(applicants_emails)

@mcp.tool()
def get_next_exam_date():
    """
    Get the next available exam date from the calendar.

    Returns:
        str: The next exam date in ISO format.
            Example: "2024-06-15T10:00:00"
    """
    return calendar.get_next_exam_date()

@mcp.tool()
def get_exam_end_time(start_time:str):
    """
    Calculate the end time of an exam given its start time.

    Parameters:
        start_time (str): The start time of the exam in ISO format.
            Example: "2024-06-15T10:00:00"

    Returns:
        str: The calculated end time in ISO format.
            Example: "2024-06-15T12:00:00"
    """
    return calendar.get_exam_end_time(start_time)

@mcp.tool()
def is_time_slot_available(date_time:str):
    """
    Check if a specific date and time slot is available for scheduling an exam.

    Parameters:
        date_time (str): The date and time to check in ISO format.
            Example: "2024-06-15T10:00:00"

    Returns:
        bool: True if the slot is available, False otherwise.
    """
    return calendar.is_time_slot_available(date_time)

@mcp.tool()
def analyze_profile(github_urls:list):
    """
    Analyze GitHub profiles for relevant skills and activity.

    Parameters:
        github_urls (list): The URL of the applicant's GitHub profile.
            Example: ["https://github.com/username", "https://github.com/username2"]

    Returns:
        list of dicts: Analysis results including skills, activity, and project highlights.
    """
    return github.analyze_profile(github_urls)

@mcp.tool()
def rank_and_select(submissions:list):
    """
    Rank and select the top applicants based on their submissions.

    Parameters:
        submissions (python list): A list of applicant submissions to be ranked.
            Example: [{"name": "John Doe", "repo_count": 1, "contribution_count": 2, "error":False}, {"name": "Jane Doe", "score": 90}]

    Returns:
        list: A ranked list of selected applicants.
    """
    return ranker.rank_and_select(submissions)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')