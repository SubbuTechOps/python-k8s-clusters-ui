
import unittest
from gke_connector import GKEConnector

class TestGKEConnector(unittest.TestCase):
    def setUp(self):
        self.connector = GKEConnector()
    
    def test_initialization(self):
        """Test that the connector initializes correctly"""
        self.assertEqual(len(self.connector.connected_clusters), 0)
        
    # TODO: Add more tests

if __name__ == '__main__':
    unittest.main()
