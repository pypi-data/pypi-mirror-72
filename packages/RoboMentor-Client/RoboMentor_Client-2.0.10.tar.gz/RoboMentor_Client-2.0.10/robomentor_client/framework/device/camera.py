import os
import time
import threading
from ..service import Requests
from ..log import Log

class Camera:

    def __init__(self, device):
        self.status = False
        self.device = device
        self.image = ""

        if not os.path.exists(device):
            return

        self.camera_task_thread = threading.Thread(target=self.camera_task)
        self.camera_task_thread.start()

    def camera_task(self):
        self.status = True
        os.system("sudo /usr/local/lib/python3.7/dist-packages/robomentor_client/framework/micro/micro --device " + self.device)
        self.status = False

    def read_image(self):
        if self.status:
            try:
                read_requests = Requests.api("http://127.0.0.1:40921/camera/read", "", "", 'GET')
                read_requests_json = read_requests.json()
                self.image = read_requests_json["data"]
                time.sleep(0.4)
                return self.image
            except Exception as e:
                Log.error(str(e))
                return
