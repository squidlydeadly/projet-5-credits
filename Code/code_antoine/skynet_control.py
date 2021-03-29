from simple_pid import PID
import time


class pidList:
    pids = {}

    @staticmethod
    def get(num):
        if num not in pidList.pids:
            pidList.pids[num] = (PID(100,0,0,setpoint=0),PID(100,0,0,setpoint=0))
        return pidList.pids[num]

def clamp_intensity(val):
    max_intensity = 500
    min_intensity = -500
    return max(min(val,max_intensity),min_intensity)

class CommandIntensity:
    def __init__(self,clockwise_intensity=0,foward_intensity=0):
        self.clockwise_intensity = clockwise_intensity
        self.foward_intensity = foward_intensity

class CommandeSkynet:
    def __init__(self,robot_index,angle=0,is_clockwise=True,grandeur=0,is_foward=True,kick=False):
        self.robot_index = robot_index
        self.angle = angle
        self.is_clockwise = is_clockwise
        self.grandeur = grandeur
        self.is_foward = is_foward
        self.kick = kick
    def get_command_intensity(self):
        pid_angle,pid_grandeur = pidList.get(self.robot_index.num)

        intensity_angle = pid_angle(-self.angle if self.is_clockwise else self.angle)
        intensity_angle = clamp_intensity(intensity_angle)

        intensity_grandeur = pid_grandeur(-self.grandeur if self.is_foward == (self.angle < 90) else self.grandeur)
        intensity_grandeur = clamp_intensity(intensity_grandeur)
        return CommandIntensity(int(intensity_angle),int(intensity_grandeur))

if __name__ == "__main__":
    x = 89
    y = 100
    while(True):
        cmd = CommandeSkynet(0,angle=x,grandeur=y)
        intensity = cmd.get_command_intensity()
        print(str(intensity.clockwise_intensity) + ' ' + str(intensity.foward_intensity) )
        x-=1
        y-=1
        time.sleep(0.5)
