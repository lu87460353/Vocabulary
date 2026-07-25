"""
词汇背诵助手 - Desktop Launcher
将 React 构建好的 dist 文件夹打包为桌面应用
"""
import webview
import os
import sys
import http.server
import socketserver
import threading
import time

if getattr(sys, 'frozen', False):
    BASE = sys._MEIPASS
else:
    BASE = os.path.dirname(os.path.abspath(__file__))

DIST_DIR = os.path.join(BASE, 'dist')
PORT = 5173

def start_server():
    os.chdir(DIST_DIR)
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        httpd.serve_forever()

def main():
    threading.Thread(target=start_server, daemon=True).start()
    time.sleep(1)
    window = webview.create_window(
        title='词汇背诵助手',
        url=f"http://localhost:{PORT}",
        width=500, height=800,
        min_size=(400, 600),
    )
    webview.start(debug=False)

if __name__ == '__main__':
    main()
