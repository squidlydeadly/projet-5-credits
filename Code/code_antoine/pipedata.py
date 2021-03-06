

class PipeData:
    def __init__(self,kill=False):
        self.kill = kill

class PipeDataKill(PipeData):
    def __init__(self):
        super().__init__(True)


class PipeDataImg(PipeData):
    def __init__(self,img=[]):
        super().__init__()
        self.img = img

class PipeDataVisionInfo(PipeData):
    def __init__(self,vision_info):
        super().__init__()
        self.vision_info = vision_info
