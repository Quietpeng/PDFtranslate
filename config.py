"""
配置文件
"""

# 代理设置
PROXY_CONFIG = {
    'enable': True,  # 是否启用代理
    'http': 'http://127.0.0.1:7890',  # HTTP代理
    'https': 'http://127.0.0.1:7890',  # HTTPS代理
}

# 翻译服务设置
TRANSLATE_CONFIG = {
    'default_service': 'google',  # 默认翻译服务
    'thread_num': 4,  # 默认线程数
}

# 界面设置
GUI_CONFIG = {
    'window_size': '600x500',  # 窗口大小
    'theme': 'default',  # 界面主题
} 