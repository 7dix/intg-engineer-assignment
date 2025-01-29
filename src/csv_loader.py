import os
import csv
import logging
from typing import List, Optional
from pydantic import ValidationError
from .models import CustomerData

"""
CSVLoader is a class responsible for loading, reading, and validating the contents of a CSV file.

Attributes:
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
        
        self.filename = filename

    def load(self) -> List[CustomerData]:
        customers: List[CustomerData] = []
        with open(self.filename, 'r') as file:
            reader = csv.DictReader(file, delimiter=',')
            for row in reader:
                customer = self._read_rows(row)
                if customer:
                    customers.append(customer)
                    
        return customers
    
    def _read_rows(self, row: dict) -> Optional[CustomerData]:
        try:
            return CustomerData(
                Name=row['Name'], 
                Age=int(row['Age']), 
                Cookie=row['Cookie'], 
                BannerId=int(row['BannerId'])
            )
        except ValueError as e:
            print(f"Error in row {row}: {e}")
            return None
        
    def _log_error(self, row, error):
        logging.error(f"Validation error for row {row}: {error}")