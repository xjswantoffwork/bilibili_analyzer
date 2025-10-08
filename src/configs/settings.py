# src/config/settings.py
"""
配置管理模块
"""

import os
from dataclasses import dataclass

@dataclass
class Settings:
    """应用配置"""
    # B站API配置
    BILIBILI_API_TIMEOUT: int = 30
    REQUEST_DELAY: float = 0.5
    
    # 分析配置
    ANALYZE_VIDEO_COUNT: int = 8
    
    # 文件路径配置
    DATA_DIR: str = "data"
    
    # 日志配置
    LOG_LEVEL: str = "INFO"

settings = Settings()