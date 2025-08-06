import signal
import time
import sys
import os
import syslog
import argparse
import secrets
import subprocess
from lib import daemon
from lib import cli
from lib import worker
from lib import config
from busylight_core import KuandoLights

# Working Modes
def run_cli():
  print("DEBUG: RUNNING CLI")
  cli.run()

def run_daemon():
  print("DEBUG: RUNNTING DAEMON")
  daemon.run()

def run_worker(token, light , command):
  print("DEBUG: RUNNING WORKER")
  if token != os.environ.get("WORKER_TOKEN"):
    syslog.syslog(syslog.LOG_ERR, 
      "Worker cannot be started directly by the user.")
    sys.exit(1)
  worker.run(light, command)

# Signal handling
def handle_signal(signum, frame):
    syslog.syslog(syslog.LOG_INFO,
      f"Received {signum}. Exiting now")
    sys.exit(0)

def main():
  print("DEBUG: main() started")

  # Signal Handler
  signal.signal(signal.SIGTERM, handle_signal)

  # Argument Parser
  # will be extended for cli usage with argcomplete in the future
  parser = argparse.ArgumentParser(description="Program modes")
  subparsers = parser.add_subparsers(dest="mode", help="Choose a mode to run")
  parser.set_defaults(mode="cli")

  cli_parser = subparsers.add_parser("cli", help="Run in CLI mode")
  daemon_parser = subparsers.add_parser("daemon", help="Run in daemon mode")
  worker_parser = subparsers.add_parser("worker", help="Run in worker mode (internal)")
  
  worker_parser.add_argument("token", help="Internal token for worker authentication")
  worker_parser.add_argument("light", help="Internal light_id for worker")
  worker_parser.add_argument("command", help="Internal command for worker")

  args = parser.parse_args()
  print("DEBUG: Parsing done")

  # Syslogger    
  syslog.openlog(
    ident="busylightd",
    facility=syslog.LOG_DAEMON)
  print("DEBUG: syslogger established")

  # load config into environment 
  config.load()
  print("DEBUG: config loaded")

  if args.mode == "daemon":
    print("DEBUG: run daemon")
    run_daemon()
  elif args.mode == "worker":
    print("DEBUG: run worker")
    run_worker(args.token, args.light, args.command)
  else :
    print("DEBUG: run cli")
    run_cli()

  print("DEBUG: Everything done  ")
  print(f"DEBUG: got following mode: {args.mode}")

if __name__ == "__main__":
    main()
