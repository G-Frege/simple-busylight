import time
import sys
import os
import syslog
from busylight_core import KuandoLights
import webcolors

def run( control_light, command ):
  print("STARTING WORKERS!")
  command = "green"
  rgb = webcolors.name_to_rgb(command)
  lights = KuandoLights.all_lights()
  for light in lights:
     light_id = light.hardware.path.decode()
     if control_light == light_id:
        while True:
          print(f"STARTING LIGHT {light_id} on {command}")
          light.on(rgb)
          time.sleep(int(os.environ.get("SIGNAL_INTERVAL")))