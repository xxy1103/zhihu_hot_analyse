"""
Flask应用启动模块
用于替换原有的response.py模块
"""

from app import app, run_flask_app
from zhihu_spider import log

def run(host='0.0.0.0', port=5251, debug=False):
    """
    启动Flask应用的主函数
    
    参数:
        host (str): 服务器主机地址，默认为'0.0.0.0'
        port (int): 服务器端口，默认为5251
        debug (bool): 是否启用调试模式，默认为False
    """
    try:
        log("正在启动Flask应用...")
        run_flask_app(host=host, port=port, debug=debug)
    except KeyboardInterrupt:
        log("Flask应用被用户中断")
    except Exception as e:
        log(f"Flask应用启动失败: {e}")
        raise

def get_app():
    """获取Flask应用实例"""
    return app

if __name__ == '__main__':
    run()
