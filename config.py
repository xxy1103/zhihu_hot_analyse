import os

class Config:
    """Flask应用基础配置"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'zhihu-analytics-secret-key-2025'
    
    # API配置
    API_HOST = os.environ.get('API_HOST') or '127.0.0.1'
    API_PORT = int(os.environ.get('API_PORT') or 5251)
    
    # 调试模式
    DEBUG = os.environ.get('FLASK_DEBUG') == 'True'
    
    # 日志配置
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    
    # CORS配置
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', '*').split(',')

class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    
class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False

class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    DEBUG = True

# 配置字典
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
