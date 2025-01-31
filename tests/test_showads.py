import os
import json
import pytest
import requests
import requests_mock
from src.showads import ShowAds
from src.models import CustomerData

@pytest.fixture
def mock_showads():
    """Creates a new instance of ShowAds for each test."""
    return ShowAds()

@pytest.fixture
def sample_customers():
    """Creates sample customer data."""
    return [
        CustomerData(Name="Luke Skylwalker", Age=25, Cookie="123e4567-e89b-12d3-a456-426614174000", BannerId=10),
        CustomerData(Name="Darth Vader", Age=30, Cookie="321e4567-e89b-12d3-a456-426614174111", BannerId=20)
    ]

# Tests for the ShowAds class.

def test_authentication(mock_showads, requests_mock):
    """Test if authentication retrieves a token correctly."""
    requests_mock.post(f"{mock_showads.base_url}/auth", json={"AccessToken": "mock_token"})
    
    mock_showads._authenticate()
    
    assert mock_showads.token == "mock_token"

def test_request_with_retries(mock_showads, requests_mock):
    """Test if a request is successful without retries."""
    requests_mock.post(f"{mock_showads.base_url}/banners/show/bulk", status_code=200)

    response = mock_showads._request_with_retries(f"{mock_showads.base_url}/banners/show/bulk")
    assert response.status_code == 200

def test_paginate_customers(mock_showads, sample_customers):
    """Test if pagination correctly returns a limited set of customers."""
    result = mock_showads._paginate_customers(sample_customers, page=1, page_size=1)
    assert len(result["Data"]) == 1

def test_bulk_show_banners(mock_showads, sample_customers, requests_mock):
    """Test if bulk_show_banners successfully sends customer data."""
    requests_mock.post(f"{mock_showads.base_url}/banners/show/bulk", status_code=200)

    mock_showads.bulk_show_banners(sample_customers)
    
    assert requests_mock.called