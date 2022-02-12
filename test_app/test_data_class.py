import unittest
import pytest

from app.flightradar.data_class import Data

class TestData(unittest.TestCase):
    
    def setUp(self) -> None:    
        self.data = Data()
        self.data = self.data.run()
        
    def test_data_init(self):
        assert self.data is not None
    
    def tearDown(self) -> None:
        pass
