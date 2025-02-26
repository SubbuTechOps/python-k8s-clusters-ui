
import unittest
from eks_connector import EKSConnector

class TestEKSConnector(unittest.TestCase):
    def setUp(self):
        self.connector = EKSConnector()
    
    def test_initialization(self):
        """Test that the connector initializes correctly"""
        self.assertEqual(len(self.connector.connected_clusters), 0)
        
    # TODO: Add more tests

if __name__ == '__main__':
    unittest.main()
