import json
import os.path


class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        else:
            self.config = {}

    def __contains__(self, item):
        return item in self.config

    def __getitem__(self, item):
        if item in self.config:
            return self.config[item]
        return None

    def __setitem__(self, key, value):
        self.config[key] = value
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, sort_keys=True, indent=4, ensure_ascii=False)
