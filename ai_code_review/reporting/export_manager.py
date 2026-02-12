import json
import os
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class ExportManager:
    """
    Handles exporting reports to disk in various formats.
    """

    def export_to_json(self, report: Dict[str, Any], output_path: str):
        """
        Save report as JSON.
        """
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(report, f, indent=4)
            logger.info(f"JSON report saved to {output_path}")
        except Exception as e:
            logger.error(f"Failed to export JSON report: {e}")

    def export_to_txt(self, report: Dict[str, Any], output_path: str):
        """
        Save report as a formatted text file.
        """
        try:
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            
            summary = report.get("project_summary", {})
            scores = report.get("scores", {})
            breakdown = scores.get("issue_breakdown", {})
            files = report.get("files", [])
            ai_insights = report.get("ai_insights", [])
            
            lines = []
            lines.append("# PROJECT ANALYSIS REPORT")
            lines.append("")
            lines.append(f"Overall Score: {scores.get('overall_score', 0)}/100")
            lines.append(f"Total Files Scanned: {summary.get('total_files', 0)}")
            lines.append(f"Total Issues Found: {summary.get('total_issues', 0)}")
            lines.append("")
            lines.append("Issue Breakdown:")
            lines.append(f"Quality: {breakdown.get('quality', 0)}")
            lines.append(f"Security: {breakdown.get('security', 0)}")
            lines.append(f"Performance: {breakdown.get('performance', 0)}")
            lines.append("")
            lines.append("Top Problem Files:")
            
            # Sort files by issue count
            sorted_files = sorted(files, key=lambda x: x['issue_count'], reverse=True)
            top_files = sorted_files[:5]
            
            for f in top_files:
                fname = os.path.basename(f['file'])
                lines.append(f"* {fname} ({f['issue_count']} issues)")
            
            lines.append("")
            lines.append("## AI Recommendations:")
            lines.append("")
            
            if not ai_insights:
                lines.append("No AI recommendations generated.")
            else:
                for item in ai_insights:
                    fname = os.path.basename(item['file'])
                    suggestion = item.get('suggestion', '').strip()
                    lines.append(f"{fname}:\n{suggestion}")
                    lines.append("\n" + "-"*40 + "\n")
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(lines))
                
            logger.info(f"Text report saved to {output_path}")
            
        except Exception as e:
            logger.error(f"Failed to export TXT report: {e}")
