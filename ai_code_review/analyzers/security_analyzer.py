from .base_analyzer import BaseAnalyzer

class SecurityAnalyzer(BaseAnalyzer):
    def analyze(self, file_path: str, content: str) -> list[dict]:
        issues = []
        lines = content.splitlines()
        
        risky_calls = [
            "eval(",
            "exec(",
            "os.system(",
            "subprocess.call(",
            "pickle.load("
        ]
        
        credential_patterns = [
            "password =",
            "api_key =",
            "secret ="
        ]

        for i, line in enumerate(lines):
            # Check for risky function calls
            for call in risky_calls:
                if call in line:
                    issues.append({
                        "type": "security",
                        "severity": "high",
                        "message": f"{call.replace('(', '()')} usage detected",
                        "line": i + 1
                    })

            # Check for credentials
            for cred in credential_patterns:
                if cred in line: # Simple substring check
                    issues.append({
                        "type": "security",
                        "severity": "high",
                        "message": "Potential hardcoded credential detected",
                        "line": i + 1
                    })
                    
        return issues

