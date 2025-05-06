from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os.path
import pickle

class GoogleFormsHandler:
    def __init__(self, api_key, form_id):
        self.api_key = api_key
        self.form_id = form_id
        self.service = self._build_service()

    def _build_service(self):
        """Build the Google Forms API service."""
        creds = None
        if os.path.exists('token.pickle'):
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', ['https://www.googleapis.com/auth/forms.responses.readonly'])
                creds = flow.run_local_server(port=0)
            
            with open('token.pickle', 'wb') as token:
                pickle.dump(creds, token)

        return build('forms', 'v1', credentials=creds)

    def get_submissions(self):
        """Fetch and process form submissions."""
        try:
            result = self.service.forms().responses().list(
                formId=self.form_id
            ).execute()
            
            submissions = []
            for response in result.get('responses', []):
                submission = {
                    'email': self._get_answer(response, '56afe2c2'),
                    'name': self._get_answer(response, '257a1cfb'),
                    'github_url': self._get_answer(response, '5a99f0a8'),
                    'submission_time': response['createTime']
                }
                submissions.append(submission)
            
            return submissions        
        except Exception as e:
            print(f"Error fetching form submissions: {str(e)}")
            return str(e)

    def _get_answer(self, response, question_id):
        """Extract answer for a specific question from the response."""
        for answer in response.get('answers', {}).values():
            if answer.get('questionId') == question_id:
                return answer.get('textAnswers', {}).get('answers', [{}])[0].get('value')
        return None 

    def check_form_id(self):
        """Check if the form ID is valid."""
        try:
            result = self.service.forms().responses().list(formId="1ETzEzk_e6SwKwh4b00eS2u9xwV5OolMtF2I6F_GATqI").execute()
            print(result)
            return True
        except Exception as e:
            print(f"Error checking form ID: {str(e)}")
            return False 