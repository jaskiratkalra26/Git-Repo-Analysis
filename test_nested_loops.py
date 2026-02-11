
import unittest
from ai_code_review.analyzers.performance_analyzer import PerformanceAnalyzer

class TestNestedLoopDetection(unittest.TestCase):
    def setUp(self):
        self.analyzer = PerformanceAnalyzer()

    def test_basic_nested_loop(self):
        code = """
def my_func():
    for i in range(10):
        for j in range(10):
            print(i, j)
"""
        issues = self.analyzer.analyze("test.py", code)
        self.assertTrue(any("Possible nested loop detected" in i["message"] for i in issues), "Failed to detect basic nested loop")

    def test_sequential_loops_no_false_positive(self):
        code = """
def my_func():
    for i in range(10):
        print(i)
    
    for j in range(10):
        print(j)
"""
        issues = self.analyzer.analyze("test.py", code)
        nested_issues = [i for i in issues if "nested loop" in i["message"]]
        self.assertEqual(len(nested_issues), 0, f"False positive detected in sequential loops: {nested_issues}")

    def test_loop_inside_if_inside_loop(self):
        code = """
for i in range(10):
    if i > 5:
        for j in range(10):
            print(j)
"""
        issues = self.analyzer.analyze("test.py", code)
        self.assertTrue(any("nested loop" in i["message"] for i in issues), "Failed to detect loop inside if block inside loop")

    def test_docstring_inside_loop_false_positive(self):
        code = '''
for i in range(10):
    """
    We iterate like this:
    for j in range(10):
        print(j)
    """
    pass
'''
        issues = self.analyzer.analyze("test.py", code)
        nested_issues = [i for i in issues if "nested loop" in i["message"]]
        self.assertEqual(len(nested_issues), 0, f"False positive detected in docstring INSIDE loop: {nested_issues}")

    def test_commented_out_code_false_positive(self):
        code = """
for i in range(10):
    # for j in range(10):
    #     print(j)
    print(i)
"""
        issues = self.analyzer.analyze("test.py", code)
        nested_issues = [i for i in issues if "nested loop" in i["message"]]
        self.assertEqual(len(nested_issues), 0, f"False positive detected in comments: {nested_issues}")

if __name__ == '__main__':
    unittest.main()
