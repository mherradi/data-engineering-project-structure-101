from datetime import datetime
import requests

from util.config_handler import ConfigHandler

class ApiHandler() :
    """Class to handle API data extraction and storage."""

    def __init__(self):
        self.config_handler  = ConfigHandler()
        self.api_url         = self.config_handler.get_api_url('API')
        self.raw_dir         = self.config_handler.get_raw_dir()


    def get_data_to_csv(self) :
        print('[INFO]: Fetching new data ...')

        response = requests.get(self.api_url)

        try:
            response.raise_for_status()
            data = response.text

            # Generate filename using ISO timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            filename = f'Data_101_V1_{timestamp}.csv'

            # Ensure raw directory exists before writing.
            self.raw_dir.mkdir(parents=True, exist_ok=True)
            file_path = self.raw_dir / filename

            # Save payload to file
            with open(file_path , 'w' , newline="", encoding="utf-8") as csvfile :
                csvfile.write(data)

            print(f"[INFO]: Data successfully saved to {file_path}")

        except requests.exceptions.RequestException as e:
            print(f"[ERROR]: Failed to fetch data from API. Details: {e}")
