import time
import sys
import os
import syslog
from busylight_core import KuandoLights
from common import read_config, get_color_from_file

def main():
    config_path = "/etc/busylightd.conf"
    settings = read_config(config_path)

    max_errors = int(settings['max_errors'])
    signal_interval = int(settings['signal_interval'])
    device_retry_interval = int(settings['device_retry_interval'])

    syslog.openlog(ident="busylightd", facility=syslog.LOG_DAEMON)

    syslog.syslog(syslog.LOG_INFO,
                  f"Using {settings['color_file']} for color management. "
                  f"Change 'color_file' in {config_path} to use a different path.")

    lights = KuandoLights.all_lights()
    error_count = 0

    try:
        while True:
            try:
                if not lights:
                    lights = KuandoLights.all_lights()

                if not lights:
                    syslog.syslog(syslog.LOG_ERR,
                                  f"Found no lights, will sleep for {device_retry_interval}s. "
                                  "If you are sure that the device is connected, check the udev rules.")
                    time.sleep(device_retry_interval)
                    continue

                for light in lights:
                    light.on(get_color_from_file())

                error_count = 0

                time.sleep(signal_interval)

            except Exception as e:
                error_count += 1
                syslog.syslog(syslog.LOG_ERR, f"Halt and Catch Fire. Something went horribly wrong: {e}")
                lights = []
                if error_count >= max_errors:
                    syslog.syslog(syslog.LOG_ERR, "Too many consecutive errors. Exiting.")
                    sys.exit(1)
                time.sleep(10)

    except KeyboardInterrupt:
        syslog.syslog(syslog.LOG_INFO, "Interrupted by user, exiting.")
        sys.exit(0)


if __name__ == "__main__":
    main()
