import unittest
import config  # Assuming the config.py file is in the same directory

class TestConfig(unittest.TestCase):
    """Test class to check the configurations in config.py"""

    def test_table_configs_is_list(self):
        """Checks if 'table_configs' is a list in config.py"""
        self.assertIsInstance(config.table_configs, list, "'table_configs' should be a list.")

if __name__ == "__main__":
    unittest.main()
