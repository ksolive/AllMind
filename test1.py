import time
from datetime import datetime

try:
    import win32gui
    platform = "Windows"
except ImportError:
    platform = "macOS"
    from AppKit import NSWorkspace

def get_active_window_title_mac():
    return NSWorkspace.sharedWorkspace().frontmostApplication().localizedName()

def get_active_window_title_windows():
    return win32gui.GetWindowText(win32gui.GetForegroundWindow())

# 根据运行的平台选择合适的函数
if(platform == "Windows"):
    get_active_window_title = get_active_window_title_windows
else:
    get_active_window_title = get_active_window_title_mac

def write_log_to_file(logfile_path, log_entries):
    with open(logfile_path, 'a') as log_file:
        log_file.writelines(log_entries)
        log_file.flush()

def log_active_window_change(logfile_path, buffer_size=10, buffer_time_limit=5):
    log_entries = []
    last_window = ""
    last_write_time = time.time()
    
    while True:
        current_time = time.time()
        active_window_title = get_active_window_title()
        
        if active_window_title != last_window:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entries.append(f"[{timestamp}] | {active_window_title}\n")
            last_window = active_window_title
        
        if len(log_entries) >= buffer_size or (current_time - last_write_time >= buffer_time_limit):
            write_log_to_file(logfile_path, log_entries)
            log_entries = []
            last_write_time = current_time

        time.sleep(0.1)

# Provide a file path for your log file
log_file_path = 'active_window_log.txt'
buffer_size = 10
buffer_time_limit = 5
log_active_window_change(log_file_path, buffer_size, buffer_time_limit)