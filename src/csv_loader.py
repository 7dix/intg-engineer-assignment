import os
import csv
import logging
from typing import List, Optional
from pydantic import ValidationError
from .models import CustomerData

"""
CSVLoader is a class responsible for loading, reading, and validating the contents of a CSV file.

Args:
    filename (str): The path to the CSV file to be loaded.

Methods:
    load():
        Reads the contents of the CSV file and returns it as a string.
    
    get_filename():
        Returns the base name of the CSV file.
"""
class CSVLoader:
    def __init__(self, filename:str):
        if not os.path.isfile(filename):
            raise FileNotFoundError(f"File {filename} not found.")
        
        self._filename = filename

    def load(self) -> List[CustomerData]:
        customers: List[CustomerData] = []
        
        # Read the CSV file
        with open(self._filename, 'r') as file:
            reader = csv.DictReader(file, delimiter=',')
            # Check if the CSV file has the correct headers
            if not self._check_headers(reader.fieldnames):
                logging.error("Invalid CSV header")
                return customers
            
            # Read each row and create a CustomerData object
            for row_id, row in enumerate(reader):
                customer = self._read_row(row, row_id)
                if customer:
                    customers.append(customer)
        
        logging.info(f"CSVLoader - Loaded {len(customers)} records")
        return customers
    
    def _check_headers(self, headers: List[str]) -> bool:
        return headers == ["Name", "Age", "Cookie", "BannerId"]
    
    def _read_row(self, row: dict, row_id: int) -> Optional[CustomerData]:
        # Check if any of the fields are missing
        if row['Age'] == None or row['BannerId'] == None or row['Cookie'] == None or row['Name'] == None:
            logging.warning(f"Invalid row {row_id}: Missing fields")
            return None

        # Try to create a CustomerData object from the row
        try:
            return CustomerData(
                Name=row['Name'], 
                Age=int(row['Age']), 
                Cookie=row['Cookie'], 
                BannerId=int(row['BannerId'])
            )
        except ValidationError as e:
            error_message = [f"{error['msg']}" for error in e.errors()]
            logging.warning(f"Invalid row {row_id}: {' '.join([error for error in error_message])}")
            return None