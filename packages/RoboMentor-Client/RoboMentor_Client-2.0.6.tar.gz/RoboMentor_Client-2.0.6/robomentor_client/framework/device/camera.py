import os
import threading
from ctypes import CDLL
import ctypes

class Camera:

    def __init__(self, device):
        self.status = False
        self.device = device
        self.micro = None

        if not os.path.exists(device):
            return

        self.camera_task_thread = threading.Thread(target=self.camera_task)
        self.camera_task_thread.start()

    def camera_task(self):
        self.status = True
        self.micro = os.system("sudo /usr/local/lib/python3.7/dist-packages/robomentor_client/framework/micro/micro --device " + self.device)



