import os
from ..log import Log

class Camera:

    def __init__(self, device):
        self.status = False

        self.dir = os.path.abspath(os.path.join(os.getcwd(), ".."))

        os.system("sudo " + self.dir + "/micro/micro --device " + device)