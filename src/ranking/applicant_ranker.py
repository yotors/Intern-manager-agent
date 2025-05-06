from config import config

class ApplicantRanker:
    def __init__(self, max_interns):
        self.max_interns = max_interns

    def rank_and_select(self, submissions):
        """Rank and select applicants based on predefined criteria."""
        # Filter out invalid submissions
        valid_submissions = [
            sub for sub in submissions
            if self._is_valid_submission(sub)
        ]
        
        # Calculate scores for each applicant
        scored_applicants = []
        for submission in valid_submissions:
            score = self._calculate_score(submission)
            scored_applicants.append({
                **submission,
                'score': score
            })
        
        # Sort by score in descending order
        scored_applicants.sort(key=lambda x: x['score'], reverse=True)
        
        # Select top applicants
        selected = scored_applicants[:self.max_interns]
        
        return selected

    def _is_valid_submission(self, submission):
        """Check if a submission meets minimum requirements."""
        return (
            submission.get('repo_count', 0) >= config.MIN_REPOS and
            submission.get('contribution_count', 0) >= config.MIN_CONTRIBUTIONS and
            not submission.get('error')
        )

    def _calculate_score(self, submission):
        """Calculate a score for the applicant based on various factors."""
        score = 0
        
        # Repository count score (max 40 points)
        repo_score = min(submission.get('repo_count', 0) * 2, 40)
        score += repo_score
        
        # Contribution count score (max 40 points)
        contribution_score = min(submission.get('contribution_count', 0) / 10, 60)
        score += contribution_score
        
        return score 