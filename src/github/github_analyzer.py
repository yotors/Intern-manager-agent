from github import Github
import re
from datetime import datetime, timedelta
import requests

class GitHubAnalyzer:
    def __init__(self, token):
        self.github = Github(token)

    def analyze_profile(self, github_urls):
        """Analyze a GitHub profile and return relevant metrics."""
        try:
            # Extract username from GitHub URL
            applicants = []
            for github_url in github_urls:
                username = self._extract_username(github_url)
                if not username:
                    applicants.append( {
                        'username': username,
                        'error': 'Invalid GitHub URL',
                        'repo_count': 0,
                        'contribution_count': 0,
                        'heatmap_data': {}
                    })
                    continue

                user = self.github.get_user(username)
                
                # Get repository count
                repo_count = user.public_repos
                
                # Get contribution data
                contribution_data = self._get_contribution_data(username)

                applicants.append({
                    'repo_count': repo_count,
                    'contribution_count': contribution_data,
                    'error': None
                })
            return {"Number": len(applicants), "list":applicants}
        except Exception as e:
            return {
                'error': str(e),
                'repo_count': 0,
                'contribution_count': 0,
                'heatmap_data': {}
            }

    def _extract_username(self, url):
        """Extract GitHub username from URL."""
        patterns = [
            r'github\.com/([^/]+)',
            r'github\.com/([^/]+)/?$'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        return None

    def _get_contribution_data(self, username):
        """Gets an approximate contribution count based on public events."""
        events_url = f"https://api.github.com/users/{username}/events/public"
        total_contributions = 0
        try:
            response = requests.get(events_url)
            response.raise_for_status() 
            events = response.json()
            for event in events:
                if event.get("type") in [ 
                    "PushEvent",
                    "PullRequestEvent",
                    "IssuesEvent",
                    "CommitCommentEvent",
                    "IssueCommentEvent",
                    "CreateEvent",
                    "ForkEvent",
                ]:
                    total_contributions += 1
            return total_contributions
        except requests.exceptions.RequestException as e:
            print(f"Error fetching events: {e}")
            return 0
        