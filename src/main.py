from forms.google_forms_handler import GoogleFormsHandler
from github.github_analyzer import GitHubAnalyzer
from ranking.applicant_ranker import ApplicantRanker
from email.email_handler import EmailHandler
from calendar.exam_scheduler import ExamScheduler
from config.config import *

def main():
    # Initialize components
    forms_handler = GoogleFormsHandler(GOOGLE_API_KEY, GOOGLE_FORM_ID)
    github_analyzer = GitHubAnalyzer(GITHUB_TOKEN)
    applicant_ranker = ApplicantRanker(MAX_INTERNS)
    email_handler = EmailHandler(EMAIL_USERNAME, EMAIL_PASSWORD, SMTP_SERVER, SMTP_PORT)
    exam_scheduler = ExamScheduler()

    try:
        # 1. Fetch and analyze form submissions
        print("Fetching form submissions...")
        submissions = forms_handler.get_submissions()
        
        # 2. Analyze GitHub profiles
        print("Analyzing GitHub profiles...")
        for submission in submissions:
            github_data = github_analyzer.analyze_profile(submission['github_url'])
            submission.update(github_data)
        
        # 3. Rank and select applicants
        print("Ranking applicants...")
        selected_applicants = applicant_ranker.rank_and_select(submissions)
        
        # 4. Send confirmation emails
        print("Sending confirmation emails...")
        for applicant in selected_applicants:
            email_handler.send_confirmation_email(applicant)
            
            # 5. Schedule exam if confirmed
            if email_handler.check_confirmation(applicant['email']):
                exam_date = exam_scheduler.get_next_exam_date()
                email_handler.send_exam_schedule(applicant, exam_date)
                
    except Exception as e:
        print(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main() 