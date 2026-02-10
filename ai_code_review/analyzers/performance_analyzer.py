from .base_analyzer import BaseAnalyzer

class PerformanceAnalyzer(BaseAnalyzer):
    def analyze(self, file_path: str, content: str) -> list[dict]:
        issues = []
        lines = content.splitlines()
        
        loop_stack = [] # Stores indentation of active loops

        for i, line in enumerate(lines):
            stripped = line.strip()
            if not stripped:
                continue

            indent = len(line) - len(stripped)

            # Manage loop stack: pop loops that have closed (indentation check)
            while loop_stack and indent <= loop_stack[-1]:
                loop_stack.pop()

            # A) Deep Nesting Check
            # Assume 4 spaces per level. > 3 levels means > 12 spaces.
            if indent > 12:
                issues.append({
                    "type": "performance",
                    "severity": "medium",
                    "message": "Deep nesting detected, may impact readability/performance",
                    "line": i + 1
                })

            # B) Nested Loop Check
            if stripped.startswith("for ") and stripped.endswith(":"):
                if loop_stack:
                    issues.append({
                        "type": "performance",
                        "severity": "high",
                        "message": "Possible nested loop detected (O(n^2) risk)",
                        "line": i + 1
                    })
                
                loop_stack.append(indent)
                
        return issues

