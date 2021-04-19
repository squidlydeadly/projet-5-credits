import yaml

class Configs:
    """singleton charger et accéder aux configurations du projet

    Attributes
    ----------
    config_path : string
        Chemin du fichier de configuration
    __instance : dictionary
        Dictionnaire des valeurs contenue dans le fichier de configs

    """
    config_path='config.yaml'
    __instance=None
    def __init__(self):
        with open(Configs.config_path, "r") as f:
            Configs.__instance = yaml.safe_load(f)
    @staticmethod
    def get():
        """renvoie crée instance ou le renvoie

        Returns
        -------
        dictionary
            Dictionnaire des configs

        """
        if Configs.__instance == None:
            Configs()
        return Configs.__instance
    @staticmethod
    def save(path=''):
        """sauvegarde les configs dans un fichier yaml

        Parameters
        ----------
        path : string
            chemin de sauvegarde, prend celui de config_path si aucun défini
            

        """
        if path== '':
            path = Configs.config_path
        with open(path, "w") as f:
            yaml.dump(Configs.get(),f)

if __name__ == "__main__":
    print(Configs.get()['ROBOTS'][0])
    Configs.get()['CAMERA']['K2']=1
    Configs.save('test.yaml')
