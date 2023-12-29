import threading
import time
from datetime import datetime
import subprocess

def get_active_window_info_mac():
    script = """
    global frontApp, frontAppName, windowTitle

    set windowTitle to ""
    tell application "System Events"
        set frontApp to first application process whose frontmost is true
        set frontAppName to name of frontApp
        set windowTitle to "no window"
        tell process frontAppName
            if exists (1st window whose value of attribute "AXMain" is true) then
                tell (1st window whose value of attribute "AXMain" is true)
                    set windowTitle to value of attribute "AXTitle"
                end tell
            end if
        end tell
    end tell

    return {frontAppName, windowTitle}
    """

    try:
        result = subprocess.run(['osascript', '-e', script], capture_output=True, text=True)
        if result.returncode == 0:
            output = result.stdout.strip()
            # print(output)
            return output
        else:
            return "Error executing AppleScript"
    except Exception as e:
        return f"Error: {e}"

def write_log_to_file(logfile_path, log_entries):
    with open(logfile_path, 'a') as log_file:
        log_file.writelines(log_entries)
        log_file.flush()

def log_active_window_change(logfile_path='logtest.txt', buffer_size=10, buffer_time_limit=5):
    log_entries = []
    last_window = ""
    last_write_time = time.time()
    
    while True:
        current_time = time.time()
        active_window_title = get_active_window_info_mac()
        print(active_window_title)
        
        if active_window_title != last_window:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            log_entries.append(f"[{timestamp}] | {active_window_title}\n")
            last_window = active_window_title
        
        if len(log_entries) >= buffer_size or (current_time - last_write_time >= buffer_time_limit):
            write_log_to_file(logfile_path, log_entries)
            log_entries = []
            last_write_time = current_time

        time.sleep(0.1)


def background_task():
    while True:
        print("子线程正在运行...")
        time.sleep(0.1)  # 睡眠1秒，以便释放GIL

# 创建线程并启动
def main():
    print("主线程开始执行...")
    t = threading.Thread(target=log_active_window_change)
    t.daemon = True  # 将线程设置为守护线程，这样不会阻止主线程退出
    t.start()

    # 主线程继续执行其他工作
    for i in range(5):
        print("主线程正在运行...")
        time.sleep(0.5)
main()
print("主线程执行完毕，将在不久后退出，此时守护线程也将终止。")