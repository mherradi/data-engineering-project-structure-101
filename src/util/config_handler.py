import configparser
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parents[1] / "config" / "config.ini"

class ConfigHandler:

    """Class for Config Hanlder Functionalities."""
    def __init__(self, config_path=None):
        self.config_path = Path(config_path) if config_path else CONFIG_PATH
        self.project_root = self.config_path.resolve().parents[2]
        self.config = configparser.ConfigParser()

        if not self.config.read(self.config_path):
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
        

    def get_api_url(self, api_name):
        """Extracts API Url from config file."""
        return self.config.get(api_name, 'url')

    def _get_project_path(self, option):
        """Return a configured project-relative path as an absolute Path."""
        path = Path(self.config.get("Paths", option))
        return path if path.is_absolute() else self.project_root / path

    def get_raw_dir(self):
        """Extracts raw directory path from config file."""
        return self._get_project_path("raw_dir")

    def get_curated_dir(self):
        """Extracts curated directory path from config file."""
        return self._get_project_path("curated_dir")

    def get_registry_file(self):
        """Extracts registry file path from config file."""
        return self._get_project_path("registry_file")
