# -*- coding: utf-8 -*-

import sys
from .framework import Init, Log, System, Serial, GPIO, Camera, Socket

if len(sys.argv) < 3:
    sys.exit(0)