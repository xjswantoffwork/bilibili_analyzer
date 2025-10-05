#!/usr/bin/env python3
"""
核心服务模块
包含基础设施层、数据层、业务层、表现层的实现
"""

import numpy as np
import json
import os
from datetime import datetime
from bilibili_api import video, user


class InfrastructureLayer:
    """网络请求、文件操作等底层基础设施"""
    
    def __init__(self, performance_monitor):
        self.monitor = performance_monitor
    
    async def network_request(self, operation_name, coroutine):
        """带监控的网络请求"""
        self.monitor.start_operation(operation_name, "network")
        try:
            result = await coroutine
            self.monitor.end_operation(True)
            return result
        except Exception as e:
            self.monitor.end_operation(False)
            raise e
    
    def file_operation(self, operation_name, operation_func):
        """带监控的文件操作"""
        self.monitor.start_operation(operation_name, "file")
        try:
            result = operation_func()
            self.monitor.end_operation(True)
            return result
        except Exception as e:
            self.monitor.end_operation(False)
            raise e


class DataLayer:
    """数据获取、清洗、格式化"""
    
    def __init__(self, infrastructure, performance_monitor):
        self.infra = infrastructure
        self.monitor = performance_monitor
    
    async def get_video_data(self, bvid):
        """获取单个视频数据"""
        return await self.infra.network_request(f"获取视频详情_{bvid[:8]}", 
                                              video.Video(bvid=bvid).get_info())
    
    async def get_user_info(self, uid):
        """获取用户信息"""
        return await self.infra.network_request(f"获取用户信息_{uid}", 
                                              user.User(uid=uid).get_user_info())
    
    async def get_user_videos(self, uid):
        """获取用户视频列表"""
        return await self.infra.network_request(f"获取视频列表_{uid}", 
                                              user.User(uid=uid).get_videos())


class BusinessLayer:
    """核心业务逻辑和算法"""
    
    def __init__(self, performance_monitor):
        self.monitor = performance_monitor
    
    def calculate_publish_std(self, timestamps):
        """计算发布间隔标准差"""
        self.monitor.start_operation("calculate_publish_std", "data_processing")
        
        if len(timestamps) < 2:
            self.monitor.end_operation(True)
            return 0
        
        intervals = np.diff(sorted(timestamps))
        std_seconds = np.std(intervals)
        
        self.monitor.end_operation(True)
        return std_seconds
    
    def calculate_triple_rates(self, videos_data):
        """计算三连率稳定性"""
        self.monitor.start_operation("calculate_triple_rates", "data_processing")
        
        triple_rates = []
        for video in videos_data:
            view = video['view']
            if view > 0:
                triple_rate = (video['like'] + video['coin'] + video['favorite']) / view
                triple_rates.append(triple_rate)
        
        rate_std = np.std(triple_rates) if triple_rates else 0
        
        self.monitor.end_operation(True)
        return rate_std

    def calculate_time_stability(self, timestamps):
        """计算时间稳定性得分"""
        self.monitor.start_operation("calculate_time_stability", "data_processing")
        
        if len(timestamps) < 2:
            self.monitor.end_operation(True)
            return 0.5  # 中性分数
        
        intervals = np.diff(sorted(timestamps))
        std_seconds = np.std(intervals)
        
        # 基准周期：自动计算平均间隔
        avg_interval = np.mean(intervals)
        baseline_cycle = max(avg_interval, 24 * 3600)  # 至少1天
        
        # 稳定性得分：标准差越小，得分越高
        relative_volatility = std_seconds / baseline_cycle
        stability_score = 1 / (1 + relative_volatility)
        
        self.monitor.end_operation(True)
        return min(stability_score, 1.0)
    
    def calculate_quality_stability(self, videos_data):
        """计算质量稳定性得分"""
        self.monitor.start_operation("calculate_quality_stability", "data_processing")
        
        if len(videos_data) < 2:
            self.monitor.end_operation(True)
            return 0.5  # 中性分数
        
        triple_rates = []
        for video in videos_data:
            view = video['view']
            if view > 0:
                triple_rate = (video['like'] + video['coin'] + video['favorite']) / view
                triple_rates.append(triple_rate)
        
        if not triple_rates:
            self.monitor.end_operation(True)
            return 0.5
        
        rate_std = np.std(triple_rates)
        avg_rate = np.mean(triple_rates)
        
        # 稳定性得分：相对标准差越小，得分越高
        if avg_rate > 0:
            relative_std = rate_std / avg_rate
        else:
            relative_std = 1.0
            
        stability_score = 1 / (1 + relative_std)
        
        self.monitor.end_operation(True)
        return min(stability_score, 1.0)
    
    def evaluate_up_stability(self, timestamps, videos_data):
        """评估UP主运营稳定性 - DS模型核心"""
        self.monitor.start_operation("evaluate_up_stability", "data_processing")
        
        # 计算两个维度的稳定性
        time_stability = self.calculate_time_stability(timestamps)
        quality_stability = self.calculate_quality_stability(videos_data)
        
        # 综合稳定性评分（时间权重60%，质量权重40%）
        time_weight = 0.6
        quality_weight = 0.4
        overall_stability = (time_stability * time_weight + 
                           quality_stability * quality_weight)
        
        # 稳定性等级评估
        if overall_stability >= 0.8:
            stability_level = "优秀"
            level_emoji = "🏆"
        elif overall_stability >= 0.6:
            stability_level = "良好" 
            level_emoji = "⭐"
        elif overall_stability >= 0.4:
            stability_level = "一般"
            level_emoji = "📊"
        else:
            stability_level = "待提升"
            level_emoji = "💡"
        
        result = {
            "time_stability": round(time_stability, 3),
            "quality_stability": round(quality_stability, 3),
            "overall_stability": round(overall_stability, 3),
            "stability_level": stability_level,
            "level_emoji": level_emoji,
            "video_count": len(videos_data)
        }
        
        self.monitor.end_operation(True)
        return result
    
    def generate_stability_report(self, stability_result, up_name):
        """生成稳定性报告"""
        self.monitor.start_operation("generate_stability_report", "data_processing")
        
        report = []
        report.append(f"\n📊 UP主【{up_name}】运营稳定性报告")
        report.append("══════════════════════════════════════")
        
        # 时间稳定性
        time_score = stability_result["time_stability"]
        time_percent = time_score * 100
        time_bar = "█" * int(time_score * 20) + "░" * (20 - int(time_score * 20))
        report.append(f"⏰ 时间稳定性: {time_percent:.1f}% {stability_result['level_emoji']}")
        report.append(f"   {time_bar}")
        
        # 质量稳定性  
        quality_score = stability_result["quality_stability"]
        quality_percent = quality_score * 100
        quality_bar = "█" * int(quality_score * 20) + "░" * (20 - int(quality_score * 20))
        report.append(f"⭐ 质量稳定性: {quality_percent:.1f}% {stability_result['level_emoji']}")
        report.append(f"   {quality_bar}")
        
        # 综合评估
        overall_score = stability_result["overall_stability"]
        overall_percent = overall_score * 100
        overall_bar = "█" * int(overall_score * 20) + "░" * (20 - int(overall_score * 20))
        report.append(f"🏆 综合稳定性: {overall_percent:.1f}% ({stability_result['stability_level']})")
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
        
        report.append(f"\n📈 基于 {stability_result['video_count']} 个视频数据分析")
        
        self.monitor.end_operation(True)
        return "\n".join(report)


class PresentationLayer:
    """用户界面和结果显示"""
    
    def __init__(self, performance_monitor):
        self.monitor = performance_monitor
    
    def display_video_info(self, data):
        """显示视频信息"""
        self.monitor.start_operation("display_video_info", "display")
        
        try:
            publish_time = datetime.fromtimestamp(data['发布时间戳'])
            
            print(f"\n📊 视频详细信息:")
            print("=" * 60)
            print(f"🎬 BV号: {data['BV号']}")
            print(f"📺 标题: {data['标题']}")
            print(f"👤 UP主: {data['UP主']}")
            print(f"🕐 发布时间: {publish_time}")
            
            self.monitor.end_operation(True)
        except Exception as e:
            self.monitor.end_operation(False)
            raise e
    
    def display_performance_report(self):
        """显示性能报告"""
        self.monitor.start_operation("display_performance", "display")
        print(f"\n{self.monitor.get_performance_report()}")
        self.monitor.end_operation(True)