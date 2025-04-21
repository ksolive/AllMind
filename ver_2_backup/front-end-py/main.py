# main.py
import sys
import time
import threading
import platform

import webview
from webview import Window

# 托盘功能
import pystray
from pystray import MenuItem as item
from PIL import Image

# 全局快捷键 (在 Windows 下用 keyboard 库)
import keyboard

# 如果是 Windows，就导入 win32 API，方便后面设置窗体置顶
if platform.system() == 'Windows':
    import win32gui
    import win32con

# 全局变量，维护窗口可见状态
window_visible = True

class Api:
    def ask_bot(self, user_input):
        print(f"[PY] Received from front-end: {user_input}")
        return f"Echo: {user_input}"

def set_window_topmost(window: Window):
    """
    如果是 Windows 环境，则使用 win32 API 设置窗体置顶
    pywebview 的 window 对象在 Windows 上可以通过 window.gui.hwnd 获取窗口句柄
    """
    # if platform.system() == 'Windows':
    #     try:
    #         hwnd = window.gui.hwnd  # --- Changed: pywebview 的 Windows 窗口句柄
    #         # 使用 SetWindowPos 将窗口置于最顶层 (HWND_TOPMOST)
    #         win32gui.SetWindowPos(
    #             hwnd,
    #             win32con.HWND_TOPMOST,
    #             0, 0, 0, 0,
    #             win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
    #         )
    #     except Exception as e:
    #         print("Failed to set window topmost:", e)
    pass

def toggle_window(window: Window):
    """
    根据 window_visible 判断当前窗口是否显示，并切换。
    """
    global window_visible
    if window_visible:
        # 如果窗口当前可见 => 隐藏
        window.hide()
        window_visible = False
    else:
        # 如果窗口当前隐藏 => 显示并置顶
        window.show()
        # --- Changed: 显示后，再调用 set_window_topmost 置顶
        set_window_topmost(window)
        window_visible = True

def quit_app(window: Window, icon: pystray.Icon):
    """
    真正退出程序
    """
    # 先关闭窗口
    window.destroy()
    # 停止托盘
    icon.stop()
    # python 方式完全退出
    sys.exit(0)

def create_tray(window: Window):
    """
    使用 pystray 创建系统托盘图标，提供 Show/Hide 和 Quit 选项
    """
    icon_img = Image.open('icon.png')  # 你的托盘图标
    tray_icon = pystray.Icon(
        "AllMind",
        icon_img,
        "AllMind",
        menu=pystray.Menu(
            item('Show/Hide', lambda: toggle_window(window)),
            # 下方 start_tray 会修改 Quit 菜单
        )
    )
    return tray_icon

def start_tray(tray_icon: pystray.Icon, window: Window):
    """
    为 Quit 菜单项绑定一个带参函数，并启动托盘事件循环
    """
    tray_icon.menu = pystray.Menu(
        item('Show/Hide', lambda: toggle_window(window)),
        item('Quit', lambda: quit_app(window, tray_icon))
    )
    tray_icon.run()

def global_hotkey_listener(window: Window):
    """
    监听 alt+space 全局热键，在 Windows 下切换前后台
    """
    hotkey_combination = "alt+space"

    def on_hotkey():
        toggle_window(window)

    keyboard.add_hotkey(hotkey_combination, on_hotkey)

    # 保持线程存活
    while True:
        time.sleep(1)

if __name__ == '__main__':
    api = Api()

    # 创建一个无标题栏的窗口
    window = webview.create_window(
        title="AllMind PyWebView Demo",
        url='http://127.0.0.1:5000',  # 你的 Flask 服务地址
        js_api=api,
        width=600,
        height=500,
        frameless=True,   # 无边框
        easy_drag=False,
        on_top=True,     # 不置顶
        background_color = '#000000',  # 背景色,
        # transparent=True,  # 透明
    )

    # 创建托盘图标
    tray_icon = create_tray(window)

    # 启动托盘线程
    tray_thread = threading.Thread(
        target=start_tray,
        args=(tray_icon, window),
        daemon=True
    )
    tray_thread.start()

    # 启动全局快捷键监听线程
    hotkey_thread = threading.Thread(
        target=global_hotkey_listener,
        args=(window,),
        daemon=True
    )
    hotkey_thread.start()

    # --- Changed: 在启动主循环前先让窗口置顶一次(如果你想初始就显示在最前)
    # 如果你想启动时默认是隐藏，可以先注释下面两行：
    set_window_topmost(window)

    # 启动 pywebview 事件循环
    webview.start(debug=False)
