# data/models.py
"""
数据模型定义
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

class VideoStat(BaseModel):
    """视频统计数据"""
    view: int
    like: int
    coin: int
    favorite: int
    danmaku: int
    reply: int

class VideoInfo(BaseModel):
    """视频基本信息"""
    bvid: str
    title: str
    pubdate: int
    duration: int
    owner: Dict[str, Any]

class DanmakuData(BaseModel):
    """弹幕数据"""
    timestamp: float
    content: str

class UserInfo(BaseModel):
    """用户信息"""
    mid: int
    name: str
    sex: str
    face: str
    sign: str
    level: int
    following: int
    follower: int
    likes: int

class StabilityResult(BaseModel):
    """稳定性分析结果"""
    time_stability: float
    quality_stability: float
    overall_stability: float
    stability_level: str
    level_emoji: str
    video_count: int

class InteractionMetrics(BaseModel):
    """互动指标"""
    like_rate: float
    coin_rate: float
    favorite_rate: float
    danmaku_density: float
    comment_rate: float
    video_count: int
    avg_views: float

class AnalysisReport(BaseModel):
    """分析报告"""
    up_profile: Dict[str, Any]
    core_metrics: Dict[str, Any]
    content_analysis: Dict[str, Any]
    expert_diagnosis: Dict[str, Any]