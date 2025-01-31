import os
import logging
import requests
from typing import List, Optional
from .models import CustomerData
import json
from datetime import datetime, timedelta
import time

"""
ShowAds API controller class.

Attributes:
    base_url (str): Base URL for the API endpoint.
    token_file (str): File to store the access token.
    token (Optional[str]): Access token needed for subsequent API calls.
"""
class ShowAds:
    def __init__(self):
        self.base_url = "https://meiro-assignment-968918017632.europe-west1.run.app"
        self.token_file = "showads_token.json"
        self.token: Optional[str] = None
        self._load_token()
    
    # Load token from file if it exists, otherwise authenticate
    def _load_token(self):
        if not os.path.exists(self.token_file):
            self._authenticate()
        else:
            with open(self.token_file, 'r') as file:
                data = json.load(file)
                self.token = data.get("token")
                expire = data.get("expire")
                if expire and datetime.fromisoformat(expire) < datetime.now():
                    self.token = None
                    self._authenticate()

    # Save token to file
    def _save_token(self):
        with open(self.token_file, 'w') as file:
            data = {
                "token": self.token,
                "expire": (datetime.now() + timedelta(hours=24)).isoformat()
            }
            json.dump(data, file)

    # Authenticate with the API and save the token
    def _authenticate(self):
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "ProjectKey": os.getenv("PROJECT_KEY")  
        }
        response = self._request_with_retries(
            f"{self.base_url}/auth",
            headers=headers,
            data=json.dumps(data)
        )
        self.token = response.json()["AccessToken"]
        logging.info(f"ShowAds - Authenticated")
        self._save_token()
        
    """
    Reusable function for sending requests with retries.
    
    Args:
        url (str): URL to send the request to.
        method (str): HTTP method to use (default POST).
        max_retries (int): Maximum number of retries.
        timeout (int): Timeout in seconds for the request.
        **kwargs: Request headers.
    """
    def _request_with_retries(self, url, method="POST", max_retries=5, timeout=2, **kwargs):
        for attempt in range(max_retries):
            response = requests.request(method, url, timeout=timeout, **kwargs)
            if response.status_code == 200:
                return response
            elif response.status_code in [429, 500]: # Retry only on rate limit and server errors
                time.sleep(2 ** attempt)
                continue
            elif response.status_code == 401:
                self._authenticate()
            break
            
        response.raise_for_status()  # Raise an exception if all retries fail
        
    """
    Paginates list of customer data and returns parsed data ready for API call.
    
    Args:
        customers (List[CustomerData]): List of customer data.
        page (int): Page number to retrieve.
        page_size (int): Number of items per page.
    
    Returns:
        dict: Parsed customer data.
    """
    def _paginate_customers(self, customers: List[CustomerData], page: int, page_size=1000) -> dict:
        start = (page - 1) * page_size
        end = start + page_size
        
        if start >= len(customers):
            return {}
        return self._parse_customers(customers[start:end])
    
    # Parse customer data for API call
    def _parse_customers(self, customers: List[CustomerData]) -> dict:
        data = {"Data": []}
        for customer in customers:
            data["Data"].append({
                "VisitorCookie": customer.Cookie,
                "BannerId": customer.BannerId
            })
        return data
        
    # Send customer data to ShowAds API in bulk
    def bulk_show_banners(self, customers: List[CustomerData]):
        # Prepare headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        
        # Send data paginated
        page = 1
        page_size = 1000
        data = self._paginate_customers(customers, page, page_size)
        
        while data != {}:
            response = self._request_with_retries(
                f"{self.base_url}/banners/show/bulk",
                headers=headers,
                data=json.dumps(data)
            )
            logging.info(f"ShowAds banners/show/bulk page {page}/{len(customers)//page_size+1} - {response.status_code}")
            
            # Move to the next page
            page += 1
            data = self._paginate_customers(customers, page)
        
        logging.info("ShowAds banners/show/bulk - Completed")