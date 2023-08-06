import select
from ..log import Log

class Camera:

    def __init__(self, device):
        self.status = False