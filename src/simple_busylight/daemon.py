import time
import sys
import os
import syslog
import configparser
from busylight_core import KuandoLights
import webcolors


def read_config(config_path):
  config = configparser.ConfigParser()
  try:
    config.read(config_path)

    if 'settings' not in config:
      syslog.syslog(syslog.LOG_ERR, "Error: Config file missing [settings] section.")
      sys.exit(1)

    settings = config['settings']

    if 'color_file' not in settings:
      syslog.syslog(syslog.LOG_WARNING,
                    "Warn: Config file is missing 'color_file', using '/tmp/sblightd' as default")
      settings['color_file'] = '/tmp/sblightd'

    if 'default_color' not in settings:
      syslog.syslog(syslog.LOG_WARNING,
                    "Warn: Config file is missing 'default_color', using 'black' as default")
      settings['default_color'] = 'black'

    if 'max_errors' not in settings:
      syslog.syslog(syslog.LOG_WARNING,
                    "Warn: Config file is missing 'max_errors', using 3 as default")
      settings['max_errors'] = '3'

    if 'signal_interval' not in settings:
      syslog.syslog(syslog.LOG_WARNING,
                    "Warn: Config file is missing 'signal_interval', using 1 as default")
      settings['signal_interval'] = '1'

    if 'device_retry_interval' not in settings:
      syslog.syslog(syslog.LOG_WARNING,
                    "Warn: Config file is missing 'device_retry_interval', using 60 as default")
      settings['device_retry_interval'] = '60'

    return settings

  except Exception as e:
    syslog.syslog(syslog.LOG_ERR, f"Error reading config: {e}")
    sys.exit(1)


def get_color_from_file():
  color_file = settings['color_file']
  default_color = settings['default_color']

  if not os.path.exists(color_file):
    return default_color

  try:
    with open(color_file, "r") as f:
      color_str = f.read().strip().lower()

    if color_str.startswith('#') and (len(color_str) == 7 or len(color_str) == 4):
      rgb = webcolors.hex_to_rgb(color_str)
    else:
      rgb = webcolors.name_to_rgb(color_str)

    return (rgb.red, rgb.green, rgb.blue)

  except Exception as e:
    print(f"Error reading color: {e}")
    return default_color


# === Main ===

config_path = "/etc/sblightd.conf"
settings = read_config(config_path)

# Convert string config values to appropriate types
max_errors = int(settings['max_errors'])
signal_interval = int(settings['signal_interval'])
device_retry_interval = int(settings['device_retry_interval'])

syslog.syslog(syslog.LOG_INFO,
              f"Using {settings['color_file']} for color management. "
              f"Change 'color_file' in {config_path} to use a different path.")

lights = KuandoLights.all_lights()
error_count = 0

try:
  while True:
    try:
      if len(lights) == 0:
        lights = KuandoLights.all_lights()

      if len(lights) == 0:
        syslog.syslog(syslog.LOG_ERR,
                      f"Found no lights, will sleep for {device_retry_interval}s. "
                      "If you are sure that the device is connected, check the udev rules.")
        time.sleep(device_retry_interval)
        continue

      for light in lights:
        light.on(get_color_from_file())

      error_count = 0  # reset error count after success

      time.sleep(signal_interval)

    except Exception as e:
      error_count += 1
      syslog.syslog(syslog.LOG_ERR, f"Halt and Catch Fire. Something went horribly wrong: {e}")
      lights = []
      if error_count >= max_errors:
        syslog.syslog(syslog.LOG_ERR, "Too many consecutive errors. I can't help you. Exiting.")
        sys.exit(1)
      time.sleep(10)

except KeyboardInterrupt:
  sys.exit(0)
