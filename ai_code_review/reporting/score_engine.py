import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)

class ScoreEngine:
    """
    Calculates project and file scores based on static analysis issues.
    """

    def __init__(self):
        self.issue_penalties = {
            "quality": {
                "low": -1,
                "medium": -3,
                "high": -5
            },
            "security": {
                "low": -5, 
                "medium": -5,
                "high": -10
            },
            "performance": {
                "low": -2,
                "medium": -4,
                "high": -4 
            }
        }
    
    def _calculate_file_metrics(self, issues: List[Dict[str, Any]]) -> tuple[int, Dict[str, int]]:
        """
        Helper to calculate both score and issue breakdown in a single loop.
        """
        score = 100
        breakdown = {"quality": 0, "security": 0, "performance": 0}
        
        for issue in issues:
            issue_type = issue.get("type", "quality").lower()
            severity = issue.get("severity", "medium").lower()
            
            # Update breakdown
            if issue_type in breakdown:
                breakdown[issue_type] += 1
            else:
                breakdown.setdefault("other", 0)
                breakdown["other"] += 1
            
            # Calculate Penalty
            penalty = 0
            if issue_type == "quality":
                penalty = self.issue_penalties["quality"].get(severity, -1)
            elif issue_type == "security":
                if severity == "high":
                    penalty = -10
                elif severity == "medium":
                    penalty = -5
                else: 
                    penalty = -2 
            elif issue_type == "performance":
                if severity == "medium":
                    penalty = -4
                elif severity == "low":
                    penalty = -2
                else:
                    penalty = -4

            score += penalty 

        return max(0, score), breakdown

    def calculate_file_score(self, issues: List[Dict[str, Any]]) -> int:
        """
        Compute score for a single file starting from 100.
        Score cannot go below 0.
        """
        score, _ = self._calculate_file_metrics(issues)
        return score

    def calculate_project_score(self, analysis_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Calculate overall project statistics and score.
        """
        total_files = len(analysis_results)
        if total_files == 0:
            return {
                "overall_score": 100,
                "average_file_score": 100,
                "total_issues": 0,
                "issue_breakdown": {
                    "quality": 0,
                    "security": 0,
                    "performance": 0
                }
            }

        total_score = 0
        total_issues = 0
        project_breakdown = {
            "quality": 0,
            "security": 0,
            "performance": 0
        }

        for result in analysis_results:
            issues = result.get("issues", [])
            
            # Calculate both score and breakdown in one pass
            file_score, file_breakdown = self._calculate_file_metrics(issues)
            
            total_score += file_score
            total_issues += len(issues)
            
            # Aggregate breakdown
            for k, v in file_breakdown.items():
                if k in project_breakdown:
                    project_breakdown[k] += v
                else:
                    project_breakdown.setdefault("other", 0)
                    project_breakdown["other"] += v

        avg_score = int(total_score / total_files)
        
        return {
            "overall_score": avg_score,
            "average_file_score": avg_score,
            "total_issues": total_issues,
            "issue_breakdown": project_breakdown
        }
