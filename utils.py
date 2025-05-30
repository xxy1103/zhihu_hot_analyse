"""
工具模块 - 提供通用的辅助函数
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any
from zhihu_spider import log

def ensure_directory_exists(dir_path: str) -> None:
    """确保目录存在，如果不存在则创建"""
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            log(f"创建目录: {dir_path}")
    except Exception as e:
        log(f"创建目录失败 {dir_path}: {e}")
        raise

def safe_json_loads(json_str: str, default=None):
    """安全的JSON解析"""
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError) as e:
        log(f"JSON解析失败: {e}")
        return default

def safe_json_dumps(obj: Any, ensure_ascii=False, indent=None) -> str:
    """安全的JSON序列化"""
    try:
        return json.dumps(obj, ensure_ascii=ensure_ascii, indent=indent)
    except (TypeError, ValueError) as e:
        log(f"JSON序列化失败: {e}")
        return "{}"

def get_current_timestamp() -> str:
    """获取当前时间戳字符串"""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def validate_hot_item(item: Dict[str, Any]) -> bool:
    """验证热搜项目数据的完整性"""
    required_fields = ['Hash', '标题', '热度']
    
    if not isinstance(item, dict):
        return False
    
    for field in required_fields:
        if field not in item:
            log(f"热搜项目缺少必需字段: {field}")
            return False
    
    return True

def filter_valid_hot_items(hot_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """过滤出有效的热搜项目"""
    valid_items = []
    
    for item in hot_list:
        if validate_hot_item(item):
            valid_items.append(item)
        else:
            log(f"跳过无效的热搜项目: {item.get('标题', 'Unknown')}")
    
    return valid_items

def get_api_response_template(success=True, data=None, message="", error_code=None):
    """获取标准化的API响应模板"""
    response = {
        "success": success,
        "timestamp": get_current_timestamp(),
        "data": data if data is not None else {},
        "message": message
    }
    
    if not success and error_code:
        response["error_code"] = error_code
    
    return response

def log_api_request(endpoint: str, method: str, params: Dict = None):
    """记录API请求日志"""
    params_str = f" 参数: {params}" if params else ""
    log(f"API请求 - {method} {endpoint}{params_str}")

def format_file_size(size_bytes: int) -> str:
    """格式化文件大小"""
    if size_bytes == 0:
        return "0B"
    
    size_names = ["B", "KB", "MB", "GB"]
    i = 0
    while size_bytes >= 1024 and i < len(size_names) - 1:
        size_bytes /= 1024.0
        i += 1
    
    return f"{size_bytes:.2f}{size_names[i]}"

def get_file_info(file_path: str) -> Dict[str, Any]:
    """获取文件信息"""
    try:
        if not os.path.exists(file_path):
            return {"exists": False}
        
        stat = os.stat(file_path)
        return {
            "exists": True,
            "size": stat.st_size,
            "size_formatted": format_file_size(stat.st_size),
            "modified_time": datetime.fromtimestamp(stat.st_mtime).strftime("%Y-%m-%d %H:%M:%S"),
            "created_time": datetime.fromtimestamp(stat.st_ctime).strftime("%Y-%m-%d %H:%M:%S")
        }
    except Exception as e:
        log(f"获取文件信息失败 {file_path}: {e}")
        return {"exists": False, "error": str(e)}
