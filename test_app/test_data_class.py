import pytest

from app.flightradar.data_class import Data

class TestData:
    
    data = Data()
        
    def test_data_init(self):
        assert self.data is not None
        

    def tearDown(self) -> None:
        pass
