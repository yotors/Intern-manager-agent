import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from email.mime.text import MIMEText
from datetime import datetime, timedelta
import base64

# Scope for sending emails
SCOPES = ['https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.readonly']

class EmailHandler:
    def __init__(self, username, password, smtp_server, smtp_port):
        self.username = username
        self.password = password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port

    
    def get_credentials(self):
        creds = None
        if os.path.exists('token.json'): # Token is stored after first auth
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)

        # If no token or invalid token, initiate OAuth flow:
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request()) # Try to refresh the token
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'client_secret.json', SCOPES) # Path to your credentials file!
                creds = flow.run_local_server(port=0)

            # Save the token for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())
        return creds

    def send_confirmation_email(self, applicant):
        """Send confirmation email to selected applicant."""
        try:
            creds = self.get_credentials()
            body = f"""
            Dear Sitotaw,

            Congratulations! You have been selected for our internship program based on your application and GitHub profile.

            Please confirm your participation by replying to this email with "CONFIRM" in the subject line.

            Best regards,
            Internship Program Team
            """
            service = build('gmail', 'v1', credentials=creds)
            message = MIMEText(body)
            message['to'] = applicant['email']
            message['from'] = self.username
            message['subject'] = "Internship Program - Confirmation Required"

            # Crucial: base64url encode the raw message
            raw = base64.urlsafe_b64encode(message.as_bytes()).decode() # Encode as bytes, then decode for JSON

            send_message = (service.users().messages().send
                            (userId="me", body={'raw': raw}).execute())
            return True
        except Exception as error:
            print(F'An error occurred: {error}')
            return False

    def send_exam_schedule(self, applicant, exam_date):
        """Send exam schedule email to confirmed applicant."""
        try:
            creds = self.get_credentials()
            body = f"""
            Dear {applicant['name']},

            Thank you for confirming your participation in our internship program.

            Your technical exam has been scheduled for:
            Date: {exam_date.strftime('%B %d, %Y')}
            Time: {exam_date.strftime('%I:%M %p')}

            Please arrive 15 minutes before the scheduled time.

            Best regards,
            Internship Program Team
            """
            service = build('gmail', 'v1', credentials=creds)
            message = MIMEText(body)
            message['From'] = self.username
            message['To'] = applicant['email']
            message['Subject'] = "Internship Program - Exam Schedule"

            raw = base64.urlsafe_b64encode(message.as_bytes()).decode() # Encode as bytes, then decode for JSON

            send_message = (service.users().messages().send
                            (userId="me", body={'raw': raw}).execute())
            return True
        except Exception as e:
            print(f"Error sending exam schedule email: {str(e)}")
            return False

    def check_confirmation(self, applicant_email):
        """Check if applicant has confirmed via email."""
        try:
            creds = self.get_credentials()
            service = build('gmail', 'v1', credentials=creds)


            # Use the Gmail API's search function
            results = service.users().messages().list(
                userId='me',
                q=f'from:{applicant_email}'
            ).execute()
            messages = results.get('messages', [])

            return {"confirmed": len(messages) > 0, "message": messages} # Returns True if any messages found

        except Exception as e:
            print(f"Error checking confirmation: {e}")
            return {"confirmed": False}