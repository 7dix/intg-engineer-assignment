import pytest
from src.csv_loader import CSVLoader

# Tests for the CSVLoader class.

def test_not_found():
    filename = 'test_data/not_found.csv'
    with pytest.raises(FileNotFoundError):
        loader = CSVLoader(filename)
        customers = loader.load()

def test_1():
    filename = 'test_data/test_1.csv'
    loader = CSVLoader(filename)
    customers = loader.load()
    assert len(customers) == 1
    
def test_2():
    filename = 'test_data/test_2.csv'
    loader = CSVLoader(filename)
    customers = loader.load()
    assert len(customers) == 1
    
def test_load_all():
    filename = 'test_data/data.csv'
    loader = CSVLoader(filename)
    customers = loader.load()
    print(len(customers))