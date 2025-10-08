# src/data/bilibili_client.py
"""
B站API客户端封装
"""

import asyncio
from typing import List, Dict, Any, Optional
from bilibili_api import video, user

# 绝对导入
from config.settings import settings
from data.models import VideoInfo, VideoStat, UserInfo

class BilibiliClient:
    """B站API客户端"""
    
    def __init__(self, performance_monitor=None):
        self.monitor = performance_monitor
    
    async def get_user_info(self, uid: int) -> Optional[UserInfo]:
        """获取用户信息"""
        if self.monitor:
            self.monitor.start_operation(f"get_user_info_{uid}", "network")
        
        try:
            user_obj = user.User(uid=uid)
            info = await user_obj.get_user_info()
            
            result = UserInfo(
                mid=info['mid'],
                name=info['name'],
                sex=info['sex'],
                face=info['face'],
                sign=info['sign'],
                level=info['level'],
                following=info['following'],
                follower=info['follower'],
                likes=info['likes']
            )
            
            if self.monitor:
                self.monitor.end_operation(True)
            return result
            
        except Exception as e:
            if self.monitor:
                self.monitor.end_operation(False)
            print(f"❌ 获取用户信息失败: {e}")
            return None
    
    async def get_video_info(self, bvid: str) -> Optional[Dict[str, Any]]:
        """获取视频信息"""
        if self.monitor:
            self.monitor.start_operation(f"get_video_info_{bvid[:8]}", "network")
        
        try:
            video_obj = video.Video(bvid=bvid)
            info = await video_obj.get_info()
            
            result = {
                'bvid': info['bvid'],
                'title': info['title'],
                'pubdate': info['pubdate'],
                'duration': info['duration'],
                'owner': info['owner'],
                'stat': info['stat']
            }
            
            if self.monitor:
                self.monitor.end_operation(True)
            return result
            
        except Exception as e:
            if self.monitor:
                self.monitor.end_operation(False)
            print(f"❌ 获取视频信息失败 {bvid}: {e}")
            return None
    
    async def get_user_videos(self, uid: int) -> Optional[List[Dict[str, Any]]]:
        """获取用户视频列表"""
        if self.monitor:
            self.monitor.start_operation(f"get_user_videos_{uid}", "network")
        
        try:
            user_obj = user.User(uid=uid)
            videos_data = await user_obj.get_videos()
            
            # 提取视频列表
            video_list = videos_data.get('list', {}).get('vlist', []) if videos_data else []
            
            if self.monitor:
                self.monitor.end_operation(True)
            return video_list
            
        except Exception as e:
            if self.monitor:
                self.monitor.end_operation(False)
            print(f"❌ 获取用户视频列表失败: {e}")
            return None
    
    async def get_video_stat(self, bvid: str) -> Optional[VideoStat]:
        """获取视频统计数据"""
        video_info = await self.get_video_info(bvid)
        if video_info and 'stat' in video_info:
            stat = video_info['stat']
            return VideoStat(
                view=stat['view'],
                like=stat['like'],
                coin=stat['coin'],
                favorite=stat['favorite'],
                danmaku=stat['danmaku'],
                reply=stat['reply']
            )
        return None