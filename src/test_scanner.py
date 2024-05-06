# test_scanner.py

import unittest
from scanner import search_configs

class TestScanner(unittest.TestCase):
    def test_search_configs(self):
        # Define the directory to scan and configurations to search for
        test_search_root = '/path/to/test/directory'  # Modify this path accordingly
        test_configs = ['postgresql.conf', 'pg_hba.conf', 'pg_ident.conf']
        
        # Perform the search
        results = search_configs(test_search_root, test_configs)
        
        # Check if results are as expected
        # This is basic and would ideally be more specific based on your expected outcomes
        self.assertIsInstance(results, list, "Results should be a list")
        self.assertTrue(all(isinstance(item, str) for item in results), "All items in results should be strings")
        print("Test results:", results)

if __name__ == '__main__':
    unittest.main()
