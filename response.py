import http.server
import sys
import pandas as pd
from dataclasses import asdict
import json
from zhihu_spider import zhihu_hot_name



class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        # 发送200状态码，表示请求成功
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        json_data = json.dumps(asdict(zhihu_hot_name), ensure_ascii=False)
        self.wfile.write(json_data.encode('utf-8'))

    def do_POST(self):
        # 发送200状态码，表示请求成功
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()
        # You can add logic here to handle POST requests if needed

def run(server_class=http.server.HTTPServer, handler_class=MyHTTPRequestHandler):
    # 获取服务器的地址和端口，如果没有指定，则使用默认的值
    server_address = ("127.0.0.1", 5251)
    if len(sys.argv) > 1:
        server_address = (sys.argv[1], int(sys.argv[2]))
    # 创建一个服务器对象
    httpd = server_class(server_address, handler_class)
    # 打印一条信息，表示服务器已经启动
    print(f"Server running on http://{server_address[0]}:{server_address[1]}/")
    # 让服务器一直运行，直到按下Ctrl+C
    httpd.serve_forever()
