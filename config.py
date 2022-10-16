import configparser


class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(config_file)

    def __contains__(self, item):
        return item in self.config['DEFAULT']

    def __getitem__(self, item):
        if item in self.config['DEFAULT']:
            return self.config['DEFAULT'][item]
        return None

    def __setitem__(self, key, value):
        self.config['DEFAULT'][key] = value
        with open(self.config_file, 'w') as cfg:
            self.config.write(cfg)
