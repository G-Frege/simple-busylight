import time
import sys
import os
import syslog
from busylight_core import KuandoLights
import webcolors

def get_color_from_command(command):
  color_name = command
  rgb = name_to_rgb(color_name)
  return (rgb.red, rgb.green, rgb.blue)

def run( control_light, command ):
  print("STARTING WORKERS!")
  rgb = get_color_from_command(command)
  lights = KuandoLights.all_lights()
  for light in lights:
     light_id = light.hardware.path.decode()
     if control_light == light_id:
        while True:
          print(f"STARTING LIGHT {light_id} on {rgb}")
          light.on(rgb)
          time.sleep(int(os.environ.get("SIGNAL_INTERVAL")))