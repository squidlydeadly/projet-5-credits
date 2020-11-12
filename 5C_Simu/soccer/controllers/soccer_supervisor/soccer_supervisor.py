from controller import Robot 

class Camera (Robot):

    timeStep = 32

    def __init__(self):
        super(Camera, self).__init__()
        
        self.camera = self.getCamera('camera')
        self.camera.enable(4 * self.timeStep)

    def run(self):
        while True:
            message = 'avoid obstacles' 
            self.emitter.send(message.encode('utf-8'))
            if self.step(self.timeStep) == -1:
                break

    def getImage(self):
        return self.camera.getImage()

camera  = Camera()
img = camera.getImage()
print(img)
