from mcp.server.fastmcp import FastMCP
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from src.calendar.attendance import Attendance

mcp = FastMCP(title="Attendance MCP Server")
attendance = Attendance()

@mcp.tool()
def weekly_attendance(summary: str):
    """
    Get weekly attendance for a Google Meet.
    Parameters:
        summary (str): Summary of the meeting can be used as query.
        days (list): Days wanted to be checked the attendance.
    Returns:
        list: List of attendance emails for the last week.
    """
    return attendance.weekly_attendance(summary)

@mcp.tool()
def mark(attendances):
    """
    Update mark of the interns based on the attendance.
    Parameters:
        attendances (list): list of email of interns who attend the meeting

    Return:
        None
    """
    return attendance.update_meeting_marks(attendances)

if __name__ == "__main__":
    mcp.run(transport='stdio')
