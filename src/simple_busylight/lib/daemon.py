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
  env = os.environ.copy()
  env["WORKER_TOKEN"] = worker_token
  env["WORKER_LIGHT"] = light_id
  env["WORKER_COMMAND"] = command
  worker = subprocess.Popen([
  sys.argv[0],
    "worker"
  ],
  env=env )
  return worker

def startup_workers(command=None):
  print("STARTING WORKERS")
  if command is None:
    command = os.environ.get('DEFAULT_COLOR')
  lights = KuandoLights.all_lights()
  workers = {}
  for light in lights:
    light_id = light.hardware.path.decode()
    worker = start_worker(light_id, command)
    workers[light_id] = (worker, light, command)
  return workers

def clear_ctrl_msg ():
  try:
    with open(ctrl_file_path, "w") as file:
        pass
    print(f"Cleared contents of {ctrl_file_path}")
  except FileNotFoundError:
    print(f"File not found: {ctrl_file_path}")
  except PermissionError:
    print(f"Permission denied: {ctrl_file_path}")
  except Exception as e:
    print(f"An error occurred: {e}")

def get_control_msg ():
  ctrl_file_path = os.environ.get('COLOR_FILE')
  try:
    with open(ctrl_file_path, "r") as f:
      ctrl_msg = f.read().strip().lower()
      clear_ctrl_msg(ctrl_file_path)
      return ctrl_msg
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


def run():
  workers = startup_workers()
  while True:
    command = get_control_msg()
    startup_workers(command)
    if control_message:
      for worker in workers:
            worker.kill()
            start_worker(worker.value())
    time.sleep(int(os.environ.get('DAEMON_UPDATE_INTERVAL')))



