import pytest
from src.models import CustomerData
import uuid

@pytest.fixture
def sample():
    return {
        'name': 'Luke Skywalker',
        'age': 25,
        'cookie': str(uuid.uuid4()),
        'banner_id': 50
    }

# Tests for the CustomerData model.

def test_simple(sample):
    """Test if the CustomerData model is created correctly."""
    customer = CustomerData(
        Name=sample['name'], 
        Age=sample['age'], 
        Cookie=sample['cookie'],
        BannerId=sample['banner_id']
    )
    assert customer.Name == sample['name']
    assert customer.Age == sample['age']
    assert customer.Cookie == sample['cookie']
    assert customer.BannerId == sample['banner_id']
    
def test_missing_fields(sample):
    """Test missing fields in the CustomerData model."""
    with pytest.raises(ValueError):
        CustomerData(
            Name=sample['name'], 
            Age=sample['age'], 
            Cookie=sample['cookie']
        )
    with pytest.raises(ValueError):
        CustomerData(
            Name=sample['name'], 
            Age=sample['age'], 
            BannerId=sample['banner_id']
        )
    with pytest.raises(ValueError):
        CustomerData(
            Name=sample['name'], 
            Cookie=sample['cookie'],
            BannerId=sample['banner_id']
        )
    with pytest.raises(ValueError):
        CustomerData(
            Age=sample['age'], 
            Cookie=sample['cookie'],
            BannerId=sample['banner_id']
        )

def test_invalid_name(sample):
    """Test invalid name in the CustomerData model."""
    with pytest.raises(ValueError):
        CustomerData(
            Name=f"{sample['name']}1", 
            Age=sample['age'],
            Cookie=sample['cookie'],
            BannerId=sample['banner_id']
        )

def test_invalid_age(sample):
    """Test invalid age in the CustomerData model."""
    with pytest.raises(ValueError):
        CustomerData(
            Name=sample['name'], 
            Age=10, 
            Cookie=sample['cookie'],
            BannerId=sample['banner_id']
        )

def test_invalid_cookie(sample):
    """Test invalid cookie in the CustomerData model."""
    with pytest.raises(ValueError):
        CustomerData(
            Name=sample['name'], 
            Age=sample['age'], 
            Cookie='invalid',
            BannerId=sample['banner_id']
        )

def test_invalid_banner_id(sample):
    """Test invalid banner ID in the CustomerData model."""
    with pytest.raises(ValueError):
        CustomerData(
            Name=sample['name'], 
            Age=sample['age'], 
            Cookie=sample['cookie'],
            BannerId=101
        )
    with pytest.raises(ValueError):
        CustomerData(
            Name=sample['name'], 
            Age=sample['age'], 
            Cookie=sample['cookie'],
            BannerId=-1
        )