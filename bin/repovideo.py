#!/usr/bin/env python3
import sys
import os
import subprocess
import argparse

# Resolve script path directory
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPTS_DIR = os.path.join(BASE_DIR, "scripts")

def main():
    parser = argparse.ArgumentParser(
        description="repovideo CLI - Universal Autonomous AI Video Producer Tool",
        usage="repovideo <command> [<args>]"
    )
    parser.add_argument("command", help="Subcommand to run (analyze, voice, record, stitch)")
    
    # Parse the command first
    args = parser.parse_known_args(sys.argv[1:2])
    if not args[0].command:
        parser.print_help()
        sys.exit(1)
        
    cmd_name = args[0].command
    cmd_args = sys.argv[2:]

    if cmd_name == "analyze":
        script_path = os.path.join(SCRIPTS_DIR, "analyze.py")
        subprocess.run([sys.executable, script_path] + cmd_args)
        
    elif cmd_name == "voice":
        script_path = os.path.join(SCRIPTS_DIR, "tts_generator.py")
        subprocess.run([sys.executable, script_path] + cmd_args)
        
    elif cmd_name == "record":
        script_path = os.path.join(SCRIPTS_DIR, "record.js")
        subprocess.run(["node", script_path] + cmd_args)
        
    elif cmd_name == "stitch":
        script_path = os.path.join(SCRIPTS_DIR, "stitch.py")
        subprocess.run([sys.executable, script_path] + cmd_args)
        
    else:
        print(f"Unknown command: {cmd_name}")
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()
