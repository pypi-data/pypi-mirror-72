import json
import os

class ConfigReader:
    
    working_dir: str
    app_name: str

    config: dict

    def __init__(
        self, 
        working_dir: str, 
        app_name: str
    ):
        super().__init__()

        self.working_dir = working_dir
        self.app_name = app_name

        self.read()

    
    def read(self):
        env_name = os.environ.get('ENV_NAME', "dev")
        config_file_path = f"{self.working_dir}/{self.app_name}.{env_name}.cfg.json"
        
        with open(config_file_path) as json_file:
            self.config = json.load(json_file)
        
        return