import sys
import os
import syslog
import configparser
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
                    "Warn: Config file is missing 'color_file', using '/tmp/busylightd' as default")
      settings['color_file'] = '/tmp/busylightd'

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



def get_color_from_file(color_file, default_color):
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


def get_control_signal(control_path):
    if not os.path.exists(control_path):
        return None
    with open(control_path, 'r') as f:
        content = f.read().strip()
    if content == '':
        return None
    return content

control_path = /tmp/busylightd.ctrl
config_path = /etc/busylight.conf
