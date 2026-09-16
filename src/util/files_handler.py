from util.config_handler import ConfigHandler

import os

from datetime import datetime


class FileHandler() :
    """Tracks and registers ingested files to prevent duplicate processing."""
    def __init__(self):
        self.config_handler = ConfigHandler()
        self.source_prefix  = 'Data_101_V1_'
        self.directory      = self.config_handler.get_raw_dir()
        self.registry_file  = self.config_handler.get_registry_file()


    def file_tracker(self) :
        
        all_files = self.list_files() 
        processed_files = self.load_registry()

        new_files = [file for file in all_files if file not in processed_files]

        self.update_registry(new_files)

        print('[INFO] Updating the registry file .. ')

        return new_files


    def list_files(self) :
        """Lists all raw CSV files matching the source prefix."""

        if not self.directory.exists():
            print(f"[WARNING]: Raw directory {self.directory} does not exist.")
            return []

        files = [ file for file in os.listdir(self.directory) if
                    file.endswith('csv')
                    and file.startswith(self.source_prefix) 
                    and os.path.isfile(os.path.join(self.directory,file))

                ]

        return files


    def load_registry(self) :
        """Loads previously processed file names from the registry file."""
        if not self.registry_file.exists() :
            # Create an empty registry if it doesn't exist yet.
            self.registry_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.registry_file ,  'w') as file :
                pass

            return set()

        with open(self.registry_file , 'r', encoding="utf-8") as file :
            return set(line.split("\t")[0] for line in file.read().splitlines())


    def update_registry(self , files) :
        """Appends newly processed files with timestamps to the registry."""
        print("[INFO]: Updating the registry file...")
        with open(self.registry_file ,'a' , encoding="utf-8") as f :
            for file in files :
                f.write(file + "\t" + datetime.now().strftime("%Y-%m-%d-%H:%M:%S") + "\n")
