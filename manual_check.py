
from ai_code_review.analyzers.performance_analyzer import PerformanceAnalyzer

code = """
for i in range(10):
    for j in range(10): # This is a nested loop
        print(i, j)
"""

analyzer = PerformanceAnalyzer()
issues = analyzer.analyze("check.py", code)
print("Issues found:", len(issues))
for i in issues:
    print(i['message'])
