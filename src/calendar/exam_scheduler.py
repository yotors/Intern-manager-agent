from datetime import datetime, timedelta
from config import config

class ExamScheduler:
    def __init__(self):
        self.scheduled_exams = []

    def get_next_exam_date(self):
        """Get the next available exam date."""
        # Start from tomorrow
        next_date = datetime.now() + timedelta(days=1)
        
        # Find the next available date that meets the buffer requirement
        while True:
            # Check if the date is a weekday (Monday to Friday)
            if next_date.weekday() < 5:  # 0 is Monday, 4 is Friday
                # Check if there's enough buffer from the last scheduled exam
                if not self.scheduled_exams or (
                    next_date - self.scheduled_exams[-1] >= timedelta(days=config.EXAM_BUFFER_DAYS)
                ):
                    # Set the exam time to 10:00 AM
                    exam_datetime = next_date.replace(
                        hour=10,
                        minute=0,
                        second=0,
                        microsecond=0
                    )
                    self.scheduled_exams.append(exam_datetime)
                    return exam_datetime
            
            # Move to the next day
            next_date += timedelta(days=1)

    def get_exam_end_time(self, start_time):
        """Get the end time for an exam given its start time."""
        return start_time + timedelta(hours=config.EXAM_DURATION_HOURS)

    def is_time_slot_available(self, date_time):
        """Check if a specific time slot is available."""
        # Check if it's a weekday
        if date_time.weekday() >= 5:  # Saturday or Sunday
            return False
        
        # Check buffer days from other exams
        for scheduled_exam in self.scheduled_exams:
            if abs(date_time - scheduled_exam) < timedelta(days=config.EXAM_BUFFER_DAYS):
                return False
        
        return True 