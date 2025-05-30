# 社交媒体数据分析平台 - Flask重构版

## 重构说明

本项目已从原有的HTTP服务器重构为使用Flask框架的现代Web应用，主要变化如下：

### 技术栈更新

- **原框架**: Python内置 `http.server`
- **新框架**: Flask + Flask-CORS
- **优势**: 更好的性能、错误处理、可扩展性和开发体验

### 文件结构

```
├── app.py              # Flask应用主文件
├── api_routes.py       # API路由定义
├── config.py           # 配置管理
├── flask_server.py     # Flask服务器启动模块
├── utils.py            # 工具函数
├── response.py         # 向后兼容模块
├── init.py             # 主启动文件（保持不变）
├── requirements.txt    # 依赖列表
├── start.bat           # Windows启动脚本
└── README_FLASK.md     # 本文档
```

### API端点

#### 原有端点（保持兼容）
- `GET /?id={hash}` - 获取特定热搜详情
- `GET /` - 获取热搜名称和热度列表

#### 新增端点
- `GET /api/hot?id={hash}` - 获取热搜数据（推荐使用）
- `GET /api/status` - 获取服务状态
- `GET /api/health` - 健康检查
- `GET /api/list` - 获取完整热搜列表（支持分页）
- `GET /api/search?keyword={keyword}` - 搜索热搜

### 配置说明

#### 环境变量
- `FLASK_ENV`: 运行环境 (development/production/testing)
- `API_HOST`: 服务器主机地址 (默认: 127.0.0.1)
- `API_PORT`: 服务器端口 (默认: 5251)
- `FLASK_DEBUG`: 调试模式 (True/False)

#### 配置类
- `DevelopmentConfig`: 开发环境配置
- `ProductionConfig`: 生产环境配置
- `TestingConfig`: 测试环境配置

### 启动方式

#### 方式1: 使用启动脚本（推荐）
```bash
start.bat
```

#### 方式2: 直接运行主文件
```bash
python init.py
```

#### 方式3: 仅启动Flask应用
```bash
python app.py
```

### 向后兼容性

- 原有的`response.py`模块已更新但保持接口不变
- `init.py`中的导入和调用方式保持不变
- 原有的API端点继续可用
- 数据处理逻辑完全不变

### 新特性

1. **更好的错误处理**: 标准化的HTTP状态码和错误消息
2. **CORS支持**: 支持跨域请求
3. **健康检查**: 便于监控和负载均衡
4. **分页支持**: 大数据量时的性能优化
5. **搜索功能**: 支持关键词搜索热搜
6. **标准化响应**: 统一的JSON响应格式
7. **配置管理**: 灵活的环境配置

### 开发建议

#### 添加新API端点
在`api_routes.py`中添加新的路由：

```python
@api_bp.route('/new-endpoint', methods=['GET'])
def new_endpoint():
    try:
        # 业务逻辑
        return jsonify({"data": "result"})
    except Exception as e:
        log(f"错误: {e}")
        return jsonify({"error": str(e)}), 500
```

#### 修改配置
在`config.py`中修改或添加配置项：

```python
class Config:
    NEW_SETTING = os.environ.get('NEW_SETTING') or 'default_value'
```

### 性能优化

1. **线程安全**: Flask支持多线程请求处理
2. **异步支持**: 可升级到Flask + asyncio
3. **缓存**: 可添加Redis或内存缓存
4. **负载均衡**: 支持多实例部署

### 安全性

1. **CORS配置**: 可配置允许的域名
2. **请求验证**: 可添加API密钥验证
3. **速率限制**: 可添加请求频率限制
4. **日志记录**: 完整的请求日志

### 故障排除

#### 常见问题
1. **端口占用**: 修改`config.py`中的`API_PORT`
2. **依赖缺失**: 运行`pip install -r requirements.txt`
3. **权限问题**: 以管理员身份运行

#### 调试模式
设置环境变量启用调试：
```bash
set FLASK_DEBUG=True
python init.py
```

### 监控和日志

- 所有日志写入`data/log/log.txt`
- API请求自动记录
- 错误信息详细记录
- 支持外部日志系统集成

---

## 迁移完成

✅ Flask框架集成完成  
✅ API端点重构完成  
✅ 向后兼容性保证  
✅ 错误处理优化  
✅ 配置管理完善  
✅ 文档和脚本齐全  

重构后的系统保持了所有原有功能，同时提供了更好的性能和开发体验。
