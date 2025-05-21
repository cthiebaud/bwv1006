#!/usr/bin/env python3
import os
import subprocess
import datetime
import sys
import time
import threading
import itertools

LOGFILE = "debug.txt"

def clear_log():
    """Clear the log file"""
    with open(LOGFILE, 'w') as f:
        pass

class TimeCounter:
    """Displays elapsed time while a process is running"""
    def __init__(self, message="Processing"):
        self.message = message
        self.running = False
        self.counter_thread = None
        self.start_time = None

    def count(self):
        self.start_time = time.time()
        try:
            while self.running:
                elapsed = time.time() - self.start_time
                minutes = int(elapsed // 60)
                seconds = int(elapsed % 60)
                tenths = int((elapsed % 1) * 10)
                
                if minutes > 0:
                    time_str = f"{minutes}m {seconds}.{tenths}s"
                else:
                    time_str = f"{seconds}.{tenths}s"
                    
                sys.stdout.write(f"\r{self.message} [{time_str} elapsed] ")
                sys.stdout.flush()
                time.sleep(0.1)
        except KeyboardInterrupt:
            # Just exit the loop if interrupted
            pass

    def start(self):
        self.running = True
        self.counter_thread = threading.Thread(target=self.count)
        self.counter_thread.daemon = True
        self.counter_thread.start()

    def stop(self):
        self.running = False
        final_time = None
        
        if self.start_time is not None:
            elapsed = time.time() - self.start_time
            minutes = int(elapsed // 60)
            seconds = int(elapsed % 60)
            tenths = int((elapsed % 1) * 10)
            
            if minutes > 0:
                final_time = f"{minutes}m {seconds}.{tenths}s"
            else:
                final_time = f"{seconds}.{tenths}s"
        
        if self.counter_thread:
            self.counter_thread.join()
            
        sys.stdout.write("\r" + " " * (len(self.message) + 30) + "\r")  # Clear the line
        sys.stdout.flush()
        
        return final_time

def log_message(message):
    """Log a message to both console and log file"""
    # timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    formatted_msg = f"▶️ {message}"
    print(formatted_msg)
    with open(LOGFILE, 'a') as f:
        f.write(formatted_msg + "\n")

def logrun(command_list):
    """Run a command and log its output"""
    cmd_str = " ".join(command_list)
    log_message(cmd_str)
    
    # Initialize counter variable before try block to ensure it exists for all exception handlers
    counter = None
    
    try:
        # Start time counter animation
        counter = TimeCounter(f"Running {command_list[0]}")
        counter.start()
        
        # Run the command and capture output
        result = subprocess.run(
            command_list,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            check=False
        )
        
        # Stop counter and get elapsed time
        elapsed_time = counter.stop()
        
        # Log the command output
        with open(LOGFILE, 'a') as f:
            f.write(result.stdout)
        print(result.stdout)
        
        # Check return code
        if result.returncode == 0:
            success_msg = f"✅ {cmd_str} (took {elapsed_time})"
            print(success_msg)
            with open(LOGFILE, 'a') as f:
                f.write(success_msg + "\n")
        else:
            error_msg = f"❌ Command failed with exit code {result.returncode}: {cmd_str} (took {elapsed_time})"
            print(error_msg)
            with open(LOGFILE, 'a') as f:
                f.write(error_msg + "\n")
            sys.exit(result.returncode)
    
    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully during command execution
        elapsed_time = None
        if counter:
            elapsed_time = counter.stop()
        
        interrupt_msg = f"\n🛑 Command interrupted by user: {cmd_str}"
        if elapsed_time:
            interrupt_msg += f" (after {elapsed_time})"
            
        print(interrupt_msg)
        with open(LOGFILE, 'a') as f:
            f.write(interrupt_msg + "\n")
        # Instead of re-raising, we'll exit with code 130
        sys.exit(130)
            
    except Exception as e:
        # Stop counter if exception occurs
        elapsed_time = None
        if counter:
            elapsed_time = counter.stop()
        
        error_msg = f"❌🛑 Exception occurred: {str(e)}"
        if elapsed_time:
            error_msg += f" (after {elapsed_time})"
            
        print(error_msg)
        with open(LOGFILE, 'a') as f:
            f.write(error_msg + "\n")
        sys.exit(1)

def main():
    # Record start time
    script_start_time = time.time()
    
    # Clear log
    clear_log()
    
    # Clean up old files
    log_message("Cleaning up old files")
    files_to_remove = [
        "bwv1006_csv_midi_note_events.csv",
        "bwv1006_csv_svg_note_heads.csv",
        "bwv1006_json_notes.json",
        "bwv1006_ly_one_line.svg",
        "bwv1006_ly_one_line.midi",
        "bwv1006.pdf",
        "bwv1006.svg"
    ]
    
    for file in files_to_remove:
        if os.path.exists(file):
            os.remove(file)
            print(f"🗑️ Removed {file}")
            with open(LOGFILE, 'a') as f:
                f.write(f"🗑️ Removed {file}\n")
    
    # Current working directory for Docker volume mapping
    current_dir = os.getcwd()
    
    # LilyPond PDF
    logrun(["docker", "run", "-v", f"{current_dir}:/work", "codello/lilypond:dev", "bwv1006.ly"])
    
    # LilyPond SVG (main)
    logrun(["docker", "run", "-v", f"{current_dir}:/work", "codello/lilypond:dev", "--svg", "bwv1006.ly"])
    
    # Remove hrefs in tabs, tighten viewbox
    logrun(["python3", "scripts/svg_remove_hrefs_in_tabs.py"])
    logrun(["python3", "scripts/svg_tighten_viewbox.py"])
    
    # LilyPond SVG (one-line)
    logrun(["docker", "run", "-v", f"{current_dir}:/work", "codello/lilypond:dev", "--svg", "bwv1006_ly_one_line.ly"])
    
    # Python processing scripts
    logrun(["python3", "scripts/midi_map.py"])
    logrun(["python3", "scripts/svg_extract_note_heads.py"])
    logrun(["python3", "scripts/align_pitch_by_geometry_simplified.py"])
    
    # Final success banner with total execution time
    script_end_time = time.time()
    total_elapsed = script_end_time - script_start_time
    minutes = int(total_elapsed // 60)
    seconds = int(total_elapsed % 60)
    tenths = int((total_elapsed % 1) * 10)
    
    if minutes > 0:
        total_time_str = f"{minutes}m {seconds}.{tenths}s"
    else:
        total_time_str = f"{seconds}.{tenths}s"
        
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    success_banner = f"\n ✅✅✅ All steps completed successfully at {timestamp} (Total time: {total_time_str}) ✅✅✅ "
    print(success_banner)
    with open(LOGFILE, 'a') as f:
        f.write(success_banner + "\n")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        # Catch keyboard interrupts at the top level in case they bubble up
        print("\n\n🛑 Process interrupted by user. Exiting gracefully...")
        with open(LOGFILE, 'a') as f:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            f.write(f"\n🛑 Process interrupted by user at {timestamp}\n")
        sys.exit(130)  # 130 is the standard exit code for Ctrl+C