from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timedelta, timezone
from config import config
from httplib2 import Http
import os.path
import os
import pickle

SCOPES = ['https://www.googleapis.com/auth/calendar']

class ExamScheduler:
    def __init__(self, calendar_id='primary'):
        self.calendar_id = calendar_id
        self.creds = self._get_credentials()
        self.service = build('calendar', 'v3', credentials=self.creds)

    def _get_credentials(self):
        creds = None
        if os.path.exists('exam_token.pickle'):
            with open('exam_token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('exam_token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def is_time_slot_available(self, date_time):
        """Check if a specific time slot is available in Google Calendar."""
        # Ensure date_time is timezone-aware and in UTC
        if date_time.tzinfo is None:
            date_time = date_time.replace(tzinfo=timezone.utc)
        start = date_time.isoformat().replace('+00:00', 'Z')
        end = (date_time + timedelta(hours=4)).isoformat().replace('+00:00', 'Z')
        events_result = self.service.events().list(
            calendarId=self.calendar_id,
            timeMin=start,
            timeMax=end,
            singleEvents=True,
            orderBy='startTime'
        ).execute()
        events = events_result.get('items', [])
        if len(events) > 0:
            return False
        return True

    def get_next_exam_date(self):
        """Get the next available exam date from Google Calendar."""
        next_date = datetime.now(timezone.utc) + timedelta(days=1)
        while True:
            if next_date.weekday() < 5:
                exam_datetime = next_date.replace(hour=10, minute=0, second=0, microsecond=0)
                if self.is_time_slot_available(exam_datetime):
                    return exam_datetime
            next_date += timedelta(days=1)
