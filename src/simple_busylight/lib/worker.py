import time
import sys
import os
import syslog
from busylight_core import KuandoLights

def run( light, command ):
   pid = os.getpid()
   print(f" Worker running ")
   print(f" Worker PID: {pid} ")
   print(f" Worker doing : {command} ond light {light} ")

