# src/core/analyzer.py
"""
核心分析模块
"""

import json
import os
import numpy as np
from datetime import datetime
from typing import List, Dict, Any, Optional

# 绝对导入
from data.bilibili_client import BilibiliClient
from data.models import StabilityResult, InteractionMetrics
from utils.performance import PerformanceMonitor

class StabilityAnalyzer:
    """稳定性分析器"""
    
    def __init__(self, performance_monitor=None):
        self.monitor = performance_monitor
    
    def calculate_time_stability(self, timestamps: List[int]) -> float:
        """计算时间稳定性得分"""
        if self.monitor:
            self.monitor.start_operation("calculate_time_stability", "data_processing")
        
        if len(timestamps) < 2:
            if self.monitor:
                self.monitor.end_operation(True)
            return 0.5
        
        try:
            intervals = np.diff(sorted(timestamps))
            std_seconds = np.std(intervals)
            avg_interval = np.mean(intervals)
            baseline_cycle = max(avg_interval, 24 * 3600)
            relative_volatility = std_seconds / baseline_cycle
            stability_score = 1 / (1 + relative_volatility)
            
            if self.monitor:
                self.monitor.end_operation(True)
            return min(stability_score, 1.0)
        except Exception:
            if self.monitor:
                self.monitor.end_operation(False)
            return 0.5
    
    def calculate_quality_stability(self, videos_data: List[Dict[str, Any]]) -> float:
        """计算质量稳定性得分"""
        if self.monitor:
            self.monitor.start_operation("calculate_quality_stability", "data_processing")
        
        if len(videos_data) < 2:
            if self.monitor:
                self.monitor.end_operation(True)
            return 0.5
        
        try:
            triple_rates = []
            for video in videos_data:
                view = video['view']
                if view > 0:
                    triple_rate = (video['like'] + video['coin'] + video['favorite']) / view
                    triple_rates.append(triple_rate)
            
            if not triple_rates:
                if self.monitor:
                    self.monitor.end_operation(True)
                return 0.5
            
            rate_std = np.std(triple_rates)
            avg_rate = np.mean(triple_rates)
            relative_std = rate_std / avg_rate if avg_rate > 0 else 1.0
            stability_score = 1 / (1 + relative_std)
            
            if self.monitor:
                self.monitor.end_operation(True)
            return min(stability_score, 1.0)
        except Exception:
            if self.monitor:
                self.monitor.end_operation(False)
            return 0.5
    
    def evaluate_up_stability(self, timestamps: List[int], videos_data: List[Dict[str, Any]]) -> StabilityResult:
        """评估UP主运营稳定性"""
        if self.monitor:
            self.monitor.start_operation("evaluate_up_stability", "data_processing")
        
        try:
            time_stability = self.calculate_time_stability(timestamps)
            quality_stability = self.calculate_quality_stability(videos_data)
            overall_stability = (time_stability * 0.6 + quality_stability * 0.4)
            
            if overall_stability >= 0.8:
                stability_level, level_emoji = "优秀", "🏆"
            elif overall_stability >= 0.6:
                stability_level, level_emoji = "良好", "⭐"
            elif overall_stability >= 0.4:
                stability_level, level_emoji = "一般", "📊"
            else:
                stability_level, level_emoji = "待提升", "💡"
            
            result = StabilityResult(
                time_stability=round(time_stability, 3),
                quality_stability=round(quality_stability, 3),
                overall_stability=round(overall_stability, 3),
                stability_level=stability_level,
                level_emoji=level_emoji,
                video_count=len(videos_data)
            )
            
            if self.monitor:
                self.monitor.end_operation(True)
            return result
        except Exception:
            if self.monitor:
                self.monitor.end_operation(False)
            return StabilityResult(
                time_stability=0.5, quality_stability=0.5, overall_stability=0.5,
                stability_level="一般", level_emoji="📊", video_count=len(videos_data)
            )
    
    def generate_stability_report(self, stability_result: StabilityResult, up_name: str) -> str:
        """生成稳定性报告"""
        if self.monitor:
            self.monitor.start_operation("generate_stability_report", "data_processing")
        
        try:
            report = []
            report.append(f"\n📊 UP主【{up_name}】运营稳定性报告")
            report.append("══════════════════════════════════════")
            
            # 时间稳定性
            time_score = stability_result.time_stability
            time_percent = time_score * 100
            time_bar = "█" * int(time_score * 20) + "░" * (20 - int(time_score * 20))
            report.append(f"⏰ 时间稳定性: {time_percent:.1f}% {stability_result.level_emoji}")
            report.append(f"   {time_bar}")
            
            # 质量稳定性  
            quality_score = stability_result.quality_stability
            quality_percent = quality_score * 100
            quality_bar = "█" * int(quality_score * 20) + "░" * (20 - int(quality_score * 20))
            report.append(f"⭐ 质量稳定性: {quality_percent:.1f}% {stability_result.level_emoji}")
            report.append(f"   {quality_bar}")
            
            # 综合评估
            overall_score = stability_result.overall_stability
            overall_percent = overall_score * 100
            overall_bar = "█" * int(overall_score * 20) + "░" * (20 - int(overall_score * 20))
            report.append(f"🏆 综合稳定性: {overall_percent:.1f}% ({stability_result.stability_level})")
            report.append(f"   {overall_bar}")
            
            # 分析建议
            report.append(f"\n💡 分析建议:")
            if overall_score >= 0.8:
                report.append("   ✅ 运营非常稳定，具备专业UP主特征")
                report.append("   💡 建议：继续保持高质量的规律更新")
            elif overall_score >= 0.6:
                report.append("   👍 运营较为稳定，有良好的内容规划")
                report.append("   💡 建议：优化发布时间规律性")
            elif overall_score >= 0.4:
                report.append("   📈 运营基本稳定，有提升空间")
                report.append("   💡 建议：加强内容质量一致性")
            else:
                report.append("   🔄 运营波动较大，建议系统规划")
                report.append("   💡 建议：建立固定的更新节奏")
            
            report.append(f"\n📈 基于 {stability_result.video_count} 个视频数据分析")
            
            if self.monitor:
                self.monitor.end_operation(True)
            return "\n".join(report)
            
        except Exception:
            if self.monitor:
                self.monitor.end_operation(False)
            return f"❌ 生成稳定性报告失败"

class InteractionAnalyzer:
    """互动分析器"""
    
    def __init__(self, benchmark_file: str = "bilibili_growth_reference.json"):
        self.benchmarks = self._load_benchmarks(benchmark_file)
    
    def _load_benchmarks(self, benchmark_file: str) -> Dict[str, Any]:
        """加载基准数据"""
        try:
            with open(benchmark_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                "startup_benchmarks": {
                    "engagement_standards": {
                        "like_rate_benchmark": 0.0436,
                        "coin_rate_benchmark": 0.0101,
                        "good_performance_threshold": 0.0499
                    }
                },
                "current_benchmarks": {
                    "engagement_standards": {
                        "like_rate_benchmark": 0.0439,
                        "coin_rate_benchmark": 0.0075,
                        "good_performance_threshold": 0.0552
                    }
                }
            }
    
    def analyze_interaction_level(self, user_videos: List[Dict[str, Any]]) -> Optional[InteractionMetrics]:
        """分析用户互动水平"""
        if not user_videos:
            return None
        
        try:
            views = [v['view'] for v in user_videos]
            likes = [v['like'] for v in user_videos]
            coins = [v['coin'] for v in user_videos]
            favorites = [v['favorite'] for v in user_videos]
            danmakus = [v.get('danmaku', 0) for v in user_videos]
            replies = [v.get('reply', 0) for v in user_videos]
            
            like_rates = [like/view for like, view in zip(likes, views) if view > 0]
            coin_rates = [coin/view for coin, view in zip(coins, views) if view > 0]
            favorite_rates = [fav/view for fav, view in zip(favorites, views) if view > 0]
            danmaku_densities = [dan/view*60 for dan, view in zip(danmakus, views) if view > 0]
            comment_rates = [reply/view for reply, view in zip(replies, views) if view > 0]
            
            return InteractionMetrics(
                like_rate=np.mean(like_rates) if like_rates else 0,
                coin_rate=np.mean(coin_rates) if coin_rates else 0,
                favorite_rate=np.mean(favorite_rates) if favorite_rates else 0,
                danmaku_density=np.mean(danmaku_densities) if danmaku_densities else 0,
                comment_rate=np.mean(comment_rates) if comment_rates else 0,
                video_count=len(user_videos),
                avg_views=np.mean(views) if views else 0
            )
        except Exception:
            return None

class BilibiliVideoAnalyzer:
    """主分析控制器"""
    
    def __init__(self):
        self.monitor = PerformanceMonitor()
        self.bilibili_client = BilibiliClient(self.monitor)
        self.stability_analyzer = StabilityAnalyzer(self.monitor)
        self.interaction_analyzer = InteractionAnalyzer()

    async def export_up_data(self, uid: int) -> bool:
        """导出UP主数据到DS模型文件"""
        print(f"🔄 正在获取UP主 {uid} 的所有视频数据...")
        
        try:
            # 1. 获取用户信息
            user_info = await self.bilibili_client.get_user_info(uid)
            if not user_info:
                print("❌ 获取用户信息失败")
                return False
                
            up_name = user_info.name
            
            # 2. 获取视频列表
            video_list = await self.bilibili_client.get_user_videos(uid)
            if not video_list:
                print("❌ 获取视频列表失败")
                return False
            
            # 3. 批量获取视频详情
            all_videos_data = []
            for video_item in video_list:
                bvid = video_item['bvid']
                video_detail = await self.bilibili_client.get_video_info(bvid)
                if video_detail:
                    video_data = {
                        "bvid": bvid,
                        "pub_timestamp": video_detail['pubdate'],
                        "view": video_detail['stat']['view'],
                        "like": video_detail['stat']['like'],
                        "coin": video_detail['stat']['coin'],
                        "favorite": video_detail['stat']['favorite'],
                        "danmaku": video_detail['stat']['danmaku'],
                        "reply": video_detail['stat']['reply']
                    }
                    all_videos_data.append(video_data)
            
            # 4. DS模型稳定性评估
            timestamps = [v['pub_timestamp'] for v in all_videos_data]
            stability_result = self.stability_analyzer.evaluate_up_stability(timestamps, all_videos_data)
            stability_report = self.stability_analyzer.generate_stability_report(stability_result, up_name)
            
            # 5. 互动水平分析
            user_metrics = self.interaction_analyzer.analyze_interaction_level(all_videos_data)
            
            # 6. 保存数据
            ds_data = {
                "metadata": {
                    "uid": str(uid),
                    "up_name": up_name,
                    "data_created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "video_count": len(all_videos_data),
                    "stability_analysis": stability_result.dict(),
                    "interaction_metrics": user_metrics.dict() if user_metrics else {}
                },
                "videos": all_videos_data
            }
            
            # 保存文件操作
            os.makedirs("data/ups", exist_ok=True)
            filename = f"data/ups/{uid}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(ds_data, f, ensure_ascii=False, indent=2)
            
            print(f"✅ DS模型数据已保存至: {filename}")
            print(f"📊 包含 {len(all_videos_data)} 个视频数据")
            
            # 7. 显示分析报告
            print(stability_report)
            if user_metrics:
                interaction_report = self.interaction_analyzer.generate_interaction_report(user_metrics, up_name)
                print(interaction_report)
            
            # 8. 显示性能报告
            print(f"\n{self.monitor.get_performance_report()}")
            
            return True
            
        except Exception as e:
            print(f"❌ 导出失败: {e}")
            return False
        
    async def analyze_up_stability(self, uid: int) -> bool:
        """仅分析UP主稳定性（不保存数据）"""
        print(f"🔄 正在分析UP主 {uid} 的运营稳定性...")
        
        try:
            # 1. 获取用户信息
            user_info = await self.bilibili_client.get_user_info(uid)
            if not user_info:
                print("❌ 获取用户信息失败")
                return False
                
            up_name = user_info.name
            
            # 2. 获取视频列表
            video_list = await self.bilibili_client.get_user_videos(uid)
            if not video_list:
                print("❌ 获取视频列表失败")
                return False
            
            # 3. 批量获取视频详情（只取最近20个视频以提高速度）
            recent_videos = video_list[:20]
            all_videos_data = []
            
            for video_item in recent_videos:
                bvid = video_item['bvid']
                video_detail = await self.bilibili_client.get_video_info(bvid)
                if video_detail:
                    video_data = {
                        "bvid": bvid,
                        "pub_timestamp": video_detail['pubdate'],
                        "view": video_detail['stat']['view'],
                        "like": video_detail['stat']['like'],
                        "coin": video_detail['stat']['coin'],
                        "favorite": video_detail['stat']['favorite']
                    }
                    all_videos_data.append(video_data)
            
            # 4. DS模型稳定性评估
            timestamps = [v['pub_timestamp'] for v in all_videos_data]
            stability_result = self.stability_analyzer.evaluate_up_stability(timestamps, all_videos_data)
            stability_report = self.stability_analyzer.generate_stability_report(stability_result, up_name)
            
            # 5. 显示稳定性报告
            print(stability_report)
            
            return True
            
        except Exception as e:
            print(f"❌ 分析失败: {e}")
            return False

    async def analyze_up_interaction(self, uid: int) -> bool:
        """分析UP主互动水平"""
        print(f"🔄 正在分析UP主 {uid} 的互动水平...")
        
        try:
            # 1. 获取用户信息
            user_info = await self.bilibili_client.get_user_info(uid)
            if not user_info:
                print("❌ 获取用户信息失败")
                return False
                
            up_name = user_info.name
            
            # 2. 获取视频列表
            video_list = await self.bilibili_client.get_user_videos(uid)
            if not video_list:
                print("❌ 获取视频列表失败")
                return False
            
            # 3. 批量获取视频详情（最近15个）
            recent_videos = video_list[:15]
            all_videos_data = []
            
            for video_item in recent_videos:
                bvid = video_item['bvid']
                video_detail = await self.bilibili_client.get_video_info(bvid)
                if video_detail:
                    video_data = {
                        "bvid": bvid,
                        "view": video_detail['stat']['view'],
                        "like": video_detail['stat']['like'],
                        "coin": video_detail['stat']['coin'],
                        "favorite": video_detail['stat']['favorite'],
                        "danmaku": video_detail['stat']['danmaku'],
                        "reply": video_detail['stat']['reply']
                    }
                    all_videos_data.append(video_data)
            
            # 4. 互动分析
            user_metrics = self.interaction_analyzer.analyze_interaction_level(all_videos_data)
            if user_metrics:
                interaction_report = self.interaction_analyzer.generate_interaction_report(
                    user_metrics, up_name
                )
                print(interaction_report)
                return True
            else:
                print("❌ 无法计算互动指标")
                return False
            
        except Exception as e:
            print(f"❌ 互动分析失败: {e}")
            return False

    async def comprehensive_analysis(self, uid: int) -> bool:
        """综合分析：稳定性 + 互动水平"""
        print(f"🔄 正在对UP主 {uid} 进行综合分析...")
        
        try:
            # 1. 获取用户信息
            user_info = await self.bilibili_client.get_user_info(uid)
            if not user_info:
                print("❌ 获取用户信息失败")
                return False
                
            up_name = user_info.name
            
            # 2. 获取视频列表
            video_list = await self.bilibili_client.get_user_videos(uid)
            if not video_list:
                print("❌ 获取视频列表失败")
                return False
            
            # 3. 批量获取视频详情（最近20个）
            recent_videos = video_list[:20]
            all_videos_data = []
            
            for video_item in recent_videos:
                bvid = video_item['bvid']
                video_detail = await self.bilibili_client.get_video_info(bvid)
                if video_detail:
                    video_data = {
                        "bvid": bvid,
                        "pub_timestamp": video_detail['pubdate'],
                        "view": video_detail['stat']['view'],
                        "like": video_detail['stat']['like'],
                        "coin": video_detail['stat']['coin'],
                        "favorite": video_detail['stat']['favorite'],
                        "danmaku": video_detail['stat']['danmaku'],
                        "reply": video_detail['stat']['reply']
                    }
                    all_videos_data.append(video_data)
            
            # 4. 稳定性评估
            timestamps = [v['pub_timestamp'] for v in all_videos_data]
            stability_result = self.stability_analyzer.evaluate_up_stability(timestamps, all_videos_data)
            stability_report = self.stability_analyzer.generate_stability_report(stability_result, up_name)
            
            # 5. 互动水平分析
            user_metrics = self.interaction_analyzer.analyze_interaction_level(all_videos_data)
            
            # 6. 显示完整报告
            print("🎯 UP主综合分析报告")
            print("=" * 60)
            print(stability_report)
            if user_metrics:
                interaction_report = self.interaction_analyzer.generate_interaction_report(user_metrics, up_name)
                print(interaction_report)
            
            return True
            
        except Exception as e:
            print(f"❌ 综合分析失败: {e}")
            return False