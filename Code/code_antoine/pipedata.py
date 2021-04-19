

class PipeData:
    """données à mettre entre les étages du pipeline

    Parameters
    ----------
    kill : bool
        est-ce que l'étage doit arrêter son exécution

    Attributes
    ----------
    kill

    """
    def __init__(self,kill=False):
        self.kill = kill

class PipeDataKill(PipeData):
    """données contenant seulement le signal pour arrêter l'étage"""

    def __init__(self):
        super().__init__(True)


class PipeDataImg(PipeData):
    """PipeData avec image

    Parameters
    ----------
    img : Image
        image à envoyer

    Attributes
    ----------
    img

    """
    def __init__(self,img=[]):
        super().__init__()
        self.img = img

class PipeDataVisionInfo(PipeData):
    """PipeData avec VisionInfo

    Parameters
    ----------
    vision_info : VisionInfo
        informations provenants de la vision

    Attributes
    ----------
    vision_info

    """
    def __init__(self,vision_info):
        super().__init__()
        self.vision_info = vision_info
