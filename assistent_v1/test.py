import os
import glob
import time
import threading
import playsound  # 用于播放音频文件

def play_and_delete_mp3(directory):
    while True:
        mp3_files = glob.glob(os.path.join(directory, '*.mp3'))
        
        if mp3_files:
            # 找到最新的MP3文件并播放
            newest_mp3 = max(mp3_files, key=os.path.getctime)
            print(f"发现新的MP3文件: {newest_mp3}")
            
            # 播放MP3文件
            playsound.playsound(newest_mp3)
            
            # 播放完毕后删除文件
            os.remove(newest_mp3)
            print(f"播放并删除文件: {newest_mp3}")
        
        time.sleep(0.2)  # 休眠一段时间后重新检查

# 开启监控线程
def monitor_directory(directory):
    monitor_thread = threading.Thread(target=play_and_delete_mp3, args=(directory,))
    monitor_thread.start()

# 监控指定目录下的MP3文件
if __name__ == "__main__":
    mp3_directory = 'voice'  # 替换成实际的目录

    monitor_directory(mp3_directory)
