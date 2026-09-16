import time
from datetime import datetime
import schedule

from util.api_handler    import ApiHandler
from util.files_handler  import FileHandler


class Scheduler() :
    """Orchestrates API ingestion and file tracking tasks at scheduled intervals."""


    def __init__(self):
        # Instantiate handlers
        self.api_handler  = ApiHandler()
        self.file_handler = FileHandler()


    def safe_api_job(self) -> None:
        """Wrapper to prevent API errors from crashing the schedule loop."""
        try:
            self.api_handler.get_data_to_csv()
        except Exception as e:
            print(f"[ERROR] [{datetime.now().strftime('%H:%M:%S')}] API Job failed: {e}")


    def safe_tracking_job(self) -> None:
        """Wrapper to process and track new files safely."""
        try:
            new_files = self.file_handler.file_tracker()
            if new_files:
                print(f"[INFO] [{datetime.now().strftime('%H:%M:%S')}] Processed files: {new_files}")
        except Exception as e:
            print(f"[ERROR] [{datetime.now().strftime('%H:%M:%S')}] Tracking Job failed: {e}")


    def start(self) -> None:
        """Schedules tasks and initiates the continuous polling loop."""
        print("--- Starting Data Engineering Scheduler ---")
        
        # Schedule jobs
        schedule.every(10).seconds.do(self.safe_api_job)
        schedule.every(1).minutes.do(self.safe_tracking_job)

        print("[INFO]: Jobs scheduled. Press Ctrl+C to stop.")

        try:
            while True:
                schedule.run_pending()
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n[INFO]: Scheduler stopped gracefully by user.")


if __name__ == "__main__":
    scheduler = Scheduler()
    scheduler.start()