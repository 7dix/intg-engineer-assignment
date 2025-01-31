from src.showads import ShowAds
from src.csv_loader import CSVLoader
import logging
from dotenv import load_dotenv

load_dotenv(override=True)

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    # Load customer data from CSV file
    csv_loader = CSVLoader("data/data.csv")
    customers = csv_loader.load()
    
    # Send customer data to ShowAds
    showads = ShowAds()
    showads.bulk_show_banners(customers)

if __name__ == "__main__":
    main()