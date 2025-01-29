import pytest
from src.models import CustomerData
import uuid

#Tests for the CustomerData model.

# default values
name = 'Luke Skywalker'
age = 25
cookie = str(uuid.uuid4())
banner_id = 50

def test_simple():
    customer = CustomerData(
        Name=name, 
        Age=age, 
        Cookie=cookie,
        BannerId=banner_id
    )
    assert customer.Name == name
    assert customer.Age == age
    assert customer.Cookie == cookie
    assert customer.BannerId == banner_id
    
def test_missing_fields():
    with pytest.raises(ValueError):
        CustomerData(
            Name=name, 
            Age=age, 
            Cookie=cookie
        )
    with pytest.raises(ValueError):
        CustomerData(
            Name=name, 
            Age=age, 
            BannerId=banner_id
        )
    with pytest.raises(ValueError):
        CustomerData(
            Name=name, 
            Cookie=cookie,
            BannerId=banner_id
        )
    with pytest.raises(ValueError):
        CustomerData(
            Age=age, 
            Cookie=cookie,
            BannerId=banner_id
        )

def test_invalid_name():
    with pytest.raises(ValueError):
        CustomerData(
            Name=f'{name}1', 
            Age=age,
            Cookie=cookie,
            BannerId=banner_id
        )

def test_invalid_age():
    with pytest.raises(ValueError):
        CustomerData(
            Name=name, 
            Age=10, 
            Cookie=cookie,
            BannerId=banner_id
        )

def test_invalid_cookie():
    with pytest.raises(ValueError):
        CustomerData(
            Name=name, 
            Age=age, 
            Cookie='invalid',
            BannerId=banner_id
        )

def test_invalid_banner_id():
    with pytest.raises(ValueError):
        CustomerData(
            Name=name, 
            Age=age, 
            Cookie=cookie,
            BannerId=101
        )
    with pytest.raises(ValueError):
        CustomerData(
            Name=name, 
            Age=age, 
            Cookie=cookie,
            BannerId=-1
        )