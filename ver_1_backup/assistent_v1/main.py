'''
开个线程运行记录程序
开个对话线程
计时初始化
循环开始
    记录输入
    扔给gpt
    打印输出
    如果有新mp3文件就播放，然后看是不是超过限制了，超了就删除所有
    到5分钟了
        开个新线程
        重新开始计时
        就从log文件里面取全部记录，喂给gpt
        删除记录

其中记录程序是log_active_window_change(logfile_path='active_window_log.txt', buffer_size=10, buffer_time_limit=5)
开个对话线程用create_thread(debug=DEBUG)
其中扔给gpt用get_completion(assistant_id, thread_id, user_input, funcs, debug=DEBUG)

'''

import threading
import time

from utils import create_assistant, create_thread, get_completion, play_and_delete_mp3, read_and_clear_file
from window_recoard_v1 import log_active_window_change
from func import tts, draw, search

import pdb


# 主循环函数
def main_loop():
    # print("debug1")
    logfile_path = 'active_window_log.txt'
    buffer_size = 10
    buffer_time_limit = 5
    assistant_id = create_assistant("ravvi")
    funcs = [tts, draw, search]
    debug = True  # 设置为 True 可以启用调试模式
    voice_dir = 'voice'
    log_path = "active_window_log.txt"
    log_max_length = 2000

    # 开始记录
    log_thread = threading.Thread(target=log_active_window_change, args=(logfile_path, buffer_size, buffer_time_limit))
    log_thread.daemon = True
    # 开声带
    voice_thread = threading.Thread(target=play_and_delete_mp3, args=(voice_dir,))
    voice_thread.daemon = True
    # 开一个会话
    thread_id = create_thread(debug)
    # 开始计时
    start_time = time.time()
    log_thread.start()
    voice_thread.start()
    print("hello")
    while True:
        # 记录输入
        user_input = input("\n--------user--------\n")
        # 扔给 GPT
        output = get_completion(assistant_id, thread_id, user_input, funcs, debug)
        tts(output)
        # 打印输出
        print("--------gpt--------\n", output)
        # 判断是否到达5分钟
        elapsed_time = time.time() - start_time
        if elapsed_time >= 5 * 60:  # 5分钟转换成秒
            log_contet = read_and_clear_file(log_path, log_max_length)
            output = get_completion(assistant_id, thread_id, log_contet, funcs, debug)
            print("--------gpt--------\n", output)
            # 开启新线程
            thread_id = create_thread(debug)
            # 重新开始计时
            start_time = time.time()
        # 休眠一段时间
        time.sleep(1)  # 暂停1秒钟，避免循环过于频繁


# pdb.set_trace()
# print("debug2")
# pdb.set_trace()
main_loop()
