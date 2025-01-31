import pytest
import csv
from src.csv_loader import CSVLoader

# Fixture to create temporary CSV files
@pytest.fixture
def create_csv(tmp_path):
    """Helper function to create a temporary CSV file."""
    def _create(filename, rows):
        path = tmp_path / filename
        with path.open("w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Name", "Age", "Cookie", "BannerId"])  # CSV Header
            writer.writerows(rows)
        return str(path)  # Return path as a string for CSVLoader
    return _create

# Tests for the CSVLoader class.

def test_file_not_found():
    """Test if FileNotFoundError is raised when file does not exist."""
    with pytest.raises(FileNotFoundError):
        loader = CSVLoader("non_existent.csv")
        loader.load()

def test_load_valid_data(create_csv):
    """Test if CSVLoader loads valid customers correctly."""
    filename = create_csv("valid.csv", [
        ["John Doe", 25, "123e4567-e89b-12d3-a456-426614174000", 10],
        ["Jane Smith", 30, "321e4567-e89b-12d3-a456-426614174111", 20]
    ])
    
    loader = CSVLoader(filename)
    customers = loader.load()
    assert len(customers) == 2  # Expecting 2 valid customers

def test_skip_invalid_rows(create_csv):
    """Test if CSVLoader skips invalid rows."""
    filename = create_csv("invalid_rows.csv", [
        ["John Doe", 10, "123e4567-e89b-12d3-a456-426614174000", -10],
        ["Valid User", 30, "321e4567-e89b-12d3-a456-426614174111", 20]
    ])
    
    loader = CSVLoader(filename)
    customers = loader.load()
    assert len(customers) == 1  # Only the valid row should be loaded

def test_empty_file(create_csv):
    """Test if an empty CSV file returns an empty list."""
    filename = create_csv("empty.csv", [])  # No data rows
    
    loader = CSVLoader(filename)
    customers = loader.load()
    assert customers == []  # Expecting empty list

def test_corrupt_file(create_csv):
    """Test if CSVLoader handles partially corrupt files and still loads valid data."""
    filename = create_csv("corrupt.csv", [
        ["John Doe", 25, "123e4567-e89b-12d3-a456-426614174000", 10],
        ["Missing Fields"],  # Corrupt row
        ["Jane Smith", 30, "321e4567-e89b-12d3-a456-426614174111", 20]
    ])
    
    loader = CSVLoader(filename)
    customers = loader.load()
    assert len(customers) == 2  # Two valid rows should be loaded