"""
自定义中间件 - 安全头配置
"""
from django.conf import settings


class SecurityHeadersMiddleware:
    """
    自定义安全头中间件
    根据环境和协议动态设置安全头
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # 检查是否为HTTPS或localhost
        is_secure = request.is_secure() or request.get_host().startswith('localhost') or request.get_host().startswith('127.0.0.1')
        
        # 只在安全环境下设置COOP头
        if is_secure and settings.IS_PROD:
            response['Cross-Origin-Opener-Policy'] = 'same-origin-allow-popups'
        
        # 其他安全头（始终设置）
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'SAMEORIGIN'
        response['X-XSS-Protection'] = '1; mode=block'
        
        # 开发环境下的额外配置
        if not settings.IS_PROD:
            # 允许开发环境的跨域访问
            response['Access-Control-Allow-Origin'] = '*'
            response['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-CSRFToken'
        
        return response

