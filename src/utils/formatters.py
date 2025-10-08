# utils/formatters.py
"""
格式化工具模块
"""

from datetime import datetime
from typing import Any, Dict

def format_timestamp(timestamp: int) -> str:
    """格式化时间戳"""
    return datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d %H:%M:%S")

def format_number(number: int) -> str:
    """格式化数字（添加千位分隔符）"""
    return f"{number:,}"

def format_percentage(value: float) -> str:
    """格式化百分比"""
    return f"{value*100:.1f}%"

def format_duration(seconds: int) -> str:
    """格式化时长"""
    if seconds < 60:
        return f"{seconds}秒"
    elif seconds < 3600:
        return f"{seconds//60}分{seconds%60}秒"
    else:
        return f"{seconds//3600}时{(seconds%3600)//60}分"

def create_progress_bar(percentage: float, width: int = 20) -> str:
    """创建进度条"""
    filled = int(percentage * width)
    empty = width - filled
    return "█" * filled + "░" * empty