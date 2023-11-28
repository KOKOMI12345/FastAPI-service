from PyQt5.QtWidgets import QApplication, QLabel, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QMessageBox
import requests
import os

class BilibiliDownloader(QWidget):
    def __init__(self):
        super().__init__()
        
        self.initUI()
        
    def initUI(self):
        # 创建控件
        self.bv_label = QLabel("B站BV号：")
        self.bv_edit = QLineEdit()
        self.audio_button = QPushButton("下载音频")
        self.video_button = QPushButton("下载视频")
        
        # 创建布局
        bv_layout = QHBoxLayout()
        bv_layout.addWidget(self.bv_label)
        bv_layout.addWidget(self.bv_edit)
        
        button_layout = QHBoxLayout()
        button_layout.addWidget(self.audio_button)
        button_layout.addWidget(self.video_button)
        
        main_layout = QVBoxLayout()
        main_layout.addLayout(bv_layout)
        main_layout.addLayout(button_layout)
        
        # 设置窗口布局
        self.setLayout(main_layout)
        
        # 信号和槽连接
        self.audio_button.clicked.connect(lambda: self.download_media('audio'))
        self.video_button.clicked.connect(lambda: self.download_media('video'))
        
        # 设置窗口标题和大小
        self.setWindowTitle("Bilibili Downloader")
        self.resize(400, 100)
        
    def download_media(self, media_type):
        # 获取BV号
        bv = self.bv_edit.text()
        
        # 发送GET请求，下载媒体文件
        url = f"https://music.cinojiang.cc/api.download?bv={bv}&returns={media_type}"
        response = requests.get(url)
        
        if response.status_code == 200:
            # 将媒体文件写入本地文件
            file_extension = "wav" if media_type == "audio" else "mp4"
            file_name = f"{bv}.{file_extension}"
            with open(file_name, "wb") as file:
                file.write(response.content)
                
            # 显示下载完成消息，并提供下载链接
            QMessageBox.information(self, "下载完成", f"{media_type}文件已成功下载！\n点击确定开始下载。")
            os.startfile(file_name)  # 打开文件所在目录
        elif response.status_code == 404:
            QMessageBox.warning(self, "下载失败", "视频或音频文件不存在。")
        elif response.status_code == 400:
            QMessageBox.warning(self, "下载失败", "无效的媒体类型。")
        else:
            QMessageBox.warning(self, "下载失败", "请求过程中出现了错误。")
        

if __name__ == '__main__':
    app = QApplication([])
    bilibili_downloader = BilibiliDownloader()
    bilibili_downloader.show()
    app.exec_()
