import sys
import os
import syslog
import configparser

def load():
  print("DEBUG: loading config now")
  config_path = "/etc/busylight.conf"
  config = configparser.ConfigParser()
  config.read(config_path)
  if 'settings' not in config:
    print("DEBUG: ERROR SET CONFIG FIRST")
    syslog.syslog(syslog.LOG_ERR, "Error: Config file missing [settings] section.")
    sys.exit(1)
  print("DEBUG: got seetings")
  settings = config['settings']
  def check_setting(key, default):
    if key not in settings:
      syslog.syslog(syslog.LOG_WARNING, f"Warn: Config missing '{key}', using default '{default}'")
      settings[key] = str(default)
  check_setting('color_file', '/tmp/busylightd')
  check_setting('default_color', 'black')
  check_setting('max_errors', 3)
  check_setting('signal_interval', 1)
  check_setting('daemon_update_interval', 60)
  print("DEBUG: loaded settings")
 
  for key, value in settings.items():
    env_key = key.upper()
    os.environ[env_key] = value
  print("DEBUG: set envoironment")

  return settings 

