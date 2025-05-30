from flask import Blueprint, jsonify, request
from dataclasses import asdict
from zhihu_spider import zhihu_hot_name, zhihu_hot_list, log

# 创建蓝图
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/hot', methods=['GET'])
def get_hot_data():
    """获取热搜数据的API端点
    
    查询参数:
    - id: 可选，热搜项目的Hash ID
    
    返回:
    - 如果没有id参数：返回所有热搜名称和热度
    - 如果有id参数：返回特定热搜的详细信息
    """
    try:
        # 获取查询参数
        id_param = request.args.get('id')
        
        if id_param is None:
            # 如果没有id参数，返回热搜名称和热度数据
            response_data = asdict(zhihu_hot_name)
            log(f"返回热搜列表，共 {len(response_data.get('name', []))} 项")
            return jsonify(response_data)
        else:
            # 如果有id参数，查找对应的热搜详情
            for item in zhihu_hot_list:
                if str(item.get('Hash')) == str(id_param):
                    log(f"返回热搜详情，ID: {id_param}, 标题: {item.get('标题', 'N/A')}")
                    return jsonify(item)
            
            # 如果没找到对应的热搜
            log(f"热搜数据未找到，ID: {id_param}")
            return jsonify({
                "error": "热搜数据未找到",
                "message": f"未找到ID为 {id_param} 的热搜数据"
            }), 404
            
    except Exception as e:
        log(f"获取热搜数据失败: {e}")
        return jsonify({
            "error": "服务器内部错误",
            "message": str(e)
        }), 500

@api_bp.route('/status', methods=['GET'])
def get_status():
    """获取服务状态"""
    try:
        status_data = {
            "status": "运行中",
            "hot_count": len(zhihu_hot_list),
            "hot_name_count": len(zhihu_hot_name.name) if hasattr(zhihu_hot_name, 'name') else 0,
            "message": "社交媒体数据分析平台API正常运行",
            "service": "zhihu-analytics",
            "version": "2.0.0-flask"
        }
        log("状态检查请求")
        return jsonify(status_data)
    except Exception as e:
        log(f"获取状态失败: {e}")
        return jsonify({
            "error": "获取状态失败",
            "message": str(e)
        }), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    """健康检查端点"""
    return jsonify({
        "status": "healthy",
        "service": "zhihu-analytics",
        "timestamp": request.headers.get('Date', 'N/A')
    })

@api_bp.route('/list', methods=['GET'])
def get_hot_list():
    """获取完整的热搜列表"""
    try:
        # 支持分页
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 50, type=int)
        
        # 计算分页
        start = (page - 1) * per_page
        end = start + per_page
        
        paginated_list = zhihu_hot_list[start:end]
        
        response_data = {
            "data": paginated_list,
            "pagination": {
                "page": page,
                "per_page": per_page,
                "total": len(zhihu_hot_list),
                "pages": (len(zhihu_hot_list) + per_page - 1) // per_page
            }
        }
        
        log(f"返回热搜列表，页码: {page}, 每页: {per_page}")
        return jsonify(response_data)
        
    except Exception as e:
        log(f"获取热搜列表失败: {e}")
        return jsonify({
            "error": "获取热搜列表失败",
            "message": str(e)
        }), 500

@api_bp.route('/search', methods=['GET'])
def search_hot():
    """搜索热搜"""
    try:
        keyword = request.args.get('keyword', '').strip()
        if not keyword:
            return jsonify({
                "error": "搜索关键词不能为空",
                "message": "请提供keyword参数"
            }), 400
        
        # 在热搜列表中搜索
        results = []
        for item in zhihu_hot_list:
            title = item.get('标题', '')
            if keyword.lower() in title.lower():
                results.append(item)
        
        log(f"搜索关键词: {keyword}, 找到 {len(results)} 条结果")
        return jsonify({
            "keyword": keyword,
            "count": len(results),
            "results": results
        })
        
    except Exception as e:
        log(f"搜索失败: {e}")
        return jsonify({
            "error": "搜索失败",
            "message": str(e)
        }), 500
