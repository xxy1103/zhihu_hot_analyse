"""
向后兼容的响应模块
重构后使用Flask框架，但保持原有接口不变
"""

from flask_server import run as flask_run
from zhihu_spider import log

# 保持向后兼容的run函数
def run(server_class=None, handler_class=None):
    """
    保持向后兼容的run函数
    现在使用Flask框架替代原有的HTTP服务器
    
    参数:
        server_class: 兼容性参数，已不使用
        handler_class: 兼容性参数，已不使用
    """
    try:
        log("使用Flask框架启动服务器...")
        # 使用默认配置启动Flask应用
        flask_run(host='0.0.0.0', port=5251, debug=False)
    except Exception as e:
        log(f"服务器启动失败: {e}")
        raise

if __name__ == '__main__':
    run()
