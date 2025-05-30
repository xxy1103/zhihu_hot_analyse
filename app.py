from flask import Flask, jsonify
from flask_cors import CORS
from api_routes import api_bp
from config import config
from zhihu_spider import log
import os

def create_app(config_name=None):
    """应用工厂函数"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    # 创建Flask应用
    app = Flask(__name__)
    
    # 加载配置
    app.config.from_object(config[config_name])
    
    # 启用CORS支持，允许跨域请求
    CORS(app, origins=app.config['CORS_ORIGINS'])
    
    # 注册蓝图
    app.register_blueprint(api_bp)
    
    # 根路径重定向
    @app.route('/')
    def index():
        return jsonify({
            "message": "社交媒体数据分析平台 API",
            "version": "2.0.0-flask",
            "endpoints": {
                "热搜数据": "/api/hot",
                "服务状态": "/api/status", 
                "健康检查": "/api/health",
                "热搜列表": "/api/list",
                "搜索热搜": "/api/search"
            }
        })
    
    return app

# 创建应用实例
app = create_app()

@app.errorhandler(404)
def not_found(error):
    """404错误处理"""
    return jsonify({"error": "API端点未找到"}), 404

@app.errorhandler(500)
def internal_error(error):
    """500错误处理"""
    log(f"服务器内部错误: {error}")
    return jsonify({"error": "服务器内部错误"}), 500

def run_flask_app(host=None, port=None, debug=None):
    """运行Flask应用"""
    try:
        # 从配置或环境变量获取参数
        host = host or app.config.get('API_HOST', '127.0.0.1')
        port = port or app.config.get('API_PORT', 5251)
        debug = debug if debug is not None else app.config.get('DEBUG', False)
        
        log(f"Flask服务器启动在 http://{host}:{port}/")
        app.run(host=host, port=port, debug=debug, threaded=True)
    except Exception as e:
        log(f"Flask服务器启动失败: {e}")
        raise

if __name__ == '__main__':
    run_flask_app()
