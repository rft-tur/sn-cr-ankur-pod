import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from t2_ast import json_to_csv

class TestJsonToCsv(unittest.TestCase):
    
    def test_ad_group_only_in_first_row(self):
        input_data = [{
            "ad_group": "AdGroup1",
            "keywords": ["kw1", "kw2"],
            "copy_title": ["title1", "title2", "title3"],
            "copy_description": ["desc1"]
        }]
        expected_csv = (
            "ad_group,keyword,copy_title,copy_description\n"
            "AdGroup1,kw1,title1,desc1\n"
            ",kw2,title2,\n"
            ",,title3,"
        )
        actual_csv = json_to_csv(input_data)
        
        actual_lines = actual_csv.splitlines()
        expected_lines = expected_csv.splitlines()
        
        self.assertEqual(len(actual_lines), len(expected_lines))
        
        for i, (actual_line, expected_line) in enumerate(zip(actual_lines, expected_lines)):
            actual_columns = actual_line.split(',')
            expected_columns = expected_line.split(',')
            self.assertEqual(
                actual_columns[0], expected_columns[0],
                f"Mismatch in ad_group column at row {i}: {actual_line} vs {expected_line}"
            )

if __name__ == "__main__":
    unittest.main()