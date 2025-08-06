import time
import sys
import os
import syslog
import secrets
import subprocess
from busylight_core import KuandoLights
import webcolors

def start_worker(light_id, command):
  worker_token = secrets.token_hex(16)
  os.environ["WORKER_TOKEN"] = worker_token
  worker = subprocess.Popen([
  sys.argv[0],
    "worker",
    worker_token,
    light_id,
    command
  ])
  return worker

def startup_workers():
  print("STARTING WORKERS")
  command = os.environ.get('DEFAULT_COLOR')
  lights = KuandoLights.all_lights()
  workers = {}
  for light in lights:
    light_id = light.hardware.path.decode()
    print(f"STARTING WORKER FOR LIGHT {light_id}")
    worker = start_worker(light_id, command)
    workers[light_id] = (worker, worker.pid, command)
  return workers

def get_control_msg ():
  ctrl_file_path = os.environ.get('COLOR_FILE')
  try:
    with open(ctrl_file_path, "r") as f:
      ctrl_msg = f.read().strip().lower()
      if ctrl_msg.startswith("#!"):
        print(f"DEBUG: Custom command detected: {ctrl_msg}")
        return ("custom_command", ctrl_msg[2:].strip())  # return type + command text
      if ctrl_msg.startswith('#') and len(ctrl_msg) in (7, 4):
        rgb = webcolors.hex_to_rgb(ctrl_msg)
        return (rgb.red, rgb.green, rgb.blue)
      if ctrl_msg.isalpha():
        rgb = webcolors.name_to_rgb(ctrl_msg)
        return (rgb.red, rgb.green, rgb.blue)
      if not ctrl_msg:
        print(f"DEBUG: No Command detected")
        return None
      print(f"DEBUG: Invalid color or command: {ctrl_msg}")
      return None

  except FileNotFoundError:
    print(f"ERROR: Color file not found: {ctrl_file_path}")
    return None
  except ValueError as e:
    print(f"ERROR: Invalid color format in {ctrl_file_path} - {e}")
    return None

def apply():
  print("DEBUG: CHANGING CONFIG")
  print("DEBUG: NOW I SHOULD CLEAR THE CONTROL FILE")

def run():
  workers = startup_workers()
  control_message = ""
  while True:
    control_message = get_control_msg()

    if control_message:
      apply()

    time.sleep(int(os.environ.get('DAEMON_UPDATE_INTERVAL')))



