import yaml

class Configs:
    config_path='config.yaml'
    __instance=None
    def __init__(self):
        with open(Configs.config_path, "r") as f:
            Configs.__instance = yaml.safe_load(f)
    @staticmethod
    def get():
        if Configs.__instance == None:
            Configs()
        return Configs.__instance
