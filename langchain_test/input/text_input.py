import sys
sys.path.append('..')
sys.path.append('../utils')

from key import OPENAI_API_KEY

import sys
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit
from PySide2.QtCore import Qt
from PySide2.QtGui import QPalette, QColor

class SpotlightApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)  # 隐藏窗口的边框
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        self.search_box = QLineEdit()
        self.search_box.setPlaceholderText("Type here...")
        self.search_box.setStyleSheet(
            "background-color: rgba(255, 255, 255, 100); border: 1px solid rgba(0, 0, 0, 100);"
            "padding: 8px;"  # 添加内边距
        )  # 设置输入框半透明背景和边框
        self.search_box.returnPressed.connect(self.test)

        font = self.search_box.font()
        font.setPointSize(24)  # 设置字体大小
        self.search_box.setFont(font)

        self.search_box.setFixedHeight(self.search_box.fontMetrics().height() * 2)
        # self.search_box.setWordWrapMode(Qt.TextWrapAnywhere) //现在不支持自动换行，要用另一个输入方法
        self.search_box.setFixedWidth(self.search_box.fontMetrics().width('a') * 50)  # 设置宽度匹配字体大小
        layout.addWidget(self.search_box)

        self.setLayout(layout)

    def test(self):
        input_text = self.search_box.text()
        print(f"Input received: {input_text}")
        # 在这里可以执行你想要的操作，例如处理输入内容、搜索文件等

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SpotlightApp()
    window.show()
    sys.exit(app.exec_())

