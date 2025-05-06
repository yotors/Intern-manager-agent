import os
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import datetime, timedelta
import pickle
import calendar as pycalendar
from googleapiclient.discovery import build as sheets_build

SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/calendar.events.readonly',
    'https://www.googleapis.com/auth/spreadsheets'
]

class Attendance:
    def __init__(self, calendar_id='primary'):
        self.calendar_id = calendar_id
        self.creds = self._get_credentials()
        self.service = build('calendar', 'v3', credentials=self.creds)

    def _get_credentials(self):
        creds = None
        if os.path.exists('attendance_token.pickle'):
            with open('attendance_token.pickle', 'rb') as token:
                creds = pickle.load(token)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            with open('attendance_token.pickle', 'wb') as token:
                pickle.dump(creds, token)
        return creds

    def weekly_attendance(self, meeting_link, day_of_week=["Monday", "Wednesday"], start_date=None, end_date=None):
        """
        Fetch attendance for a Google Meet link for meetings that occur on specific day of the week.
        """
        try:
            if not start_date:
                start_date = (datetime.utcnow() - timedelta(days=5)).isoformat() + 'Z'
            if not end_date:
                end_date = datetime.utcnow().isoformat() + 'Z'

            events_result = self.service.events().list(
                calendarId=self.calendar_id,
                timeMin=start_date,
                timeMax=end_date,
                singleEvents=True,
                orderBy='startTime',
                q=meeting_link
            ).execute()
            events = events_result.get('items', [])
            # for event in events:
            #     print(event)
            event_count = 0
            attendance = []
            for event in events:
                # Parse the event start date to check the weekday
                start_str = event.get('start', {}).get('dateTime') or event.get('start', {}).get('date')
                if start_str:
                    event_date = datetime.fromisoformat(start_str.replace('Z', '+00:00'))
                    weekday = pycalendar.day_name[event_date.weekday()]
                    if weekday not in day_of_week:
                        continue  

                event_count += 1
                attendees = event.get('attendees', [])
                for attendee in attendees:
                    attendance.append({
                        'email': attendee.get('email'),
                    })
            return {
                "EventsFound": event_count,
                "NumberOfAttendees": len(attendance),
                "Attendance": attendance
            } 
        except Exception as e:
            return {"error": str(e)}

    def update_meeting_marks(self, attendance_emails):
        """
        Update the Google Sheet to put -1 under the 'meeting' column for interns who did not attend.
        """
        sheet_id = "1xta4bU_iWmloVtdN0poTt7bJeFKlvgsCvow9ddrw3BM"
        sheet_name = "Sheet1"
        creds = self.creds
        service = sheets_build('sheets', 'v4', credentials=creds)
        sheet = service.spreadsheets()

        # Read all intern emails from the sheet
        result = sheet.values().get(
            spreadsheetId=sheet_id,
            range=f"{sheet_name}!A1:Z"  
        ).execute()
        values = result.get('values', [])
        if not values:
            print("No data found in the sheet.")
            return

        header = values[0]
        email_col = header.index('email')
        meeting_col = header.index('meeting')

        updates = []
        for i, row in enumerate(values[1:], start=2):  # start=2 because of header
            intern_email = row[email_col] if len(row) > email_col else ''
            if intern_email and intern_email not in attendance_emails:
                cell = f"{chr(65+meeting_col)}{i}"
                updates.append({
                    'range': f"{sheet_name}!{cell}",
                    'values': [[-1]]
                })

        # Batch update all missing marks
        if updates:
            body = {'valueInputOption': 'USER_ENTERED', 'data': updates}
            sheet.values().batchUpdate(
                spreadsheetId=sheet_id,
                body=body
            ).execute()
            print("Marks updated for absentees.")
        else:
            print("No absentees to update.")
        return 

