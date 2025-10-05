#!/usr/bin/env python3
"""
分析模块
包含主控制器和核心分析流程
"""

import json
import os
from datetime import datetime
from performance import PerformanceMonitor
from core_services import InfrastructureLayer, DataLayer, BusinessLayer, PresentationLayer
from interaction_analyzer import InteractionAnalyzer


class BilibiliVideoAnalyzer:
    """主控制器 - 协调各层工作"""
    
    def __init__(self):
        # 初始化各层
        self.monitor = PerformanceMonitor()
        self.infra = InfrastructureLayer(self.monitor)
        self.data_layer = DataLayer(self.infra, self.monitor)
        self.business_layer = BusinessLayer(self.monitor)
        self.presentation = PresentationLayer(self.monitor)
        self.interaction_analyzer = InteractionAnalyzer()
        
        self.data_dir = "data"
    
    async def export_up_data(self, uid):
        """导出UP主数据到DS模型文件"""
        print(f"🔄 正在获取UP主 {uid} 的所有视频数据...")
        
        try:
            # 1. 获取用户信息
            user_info = await self.data_layer.get_user_info(uid)
            up_name = user_info['name']
            
            # 2. 获取视频列表
            videos_response = await self.data_layer.get_user_videos(uid)
            video_list = videos_response['list']['vlist'] if videos_response else []
            
            # 3. 批量获取视频详情
            all_videos_data = []
            for video_item in video_list:
                bvid = video_item['bvid']
                video_detail = await self.data_layer.get_video_data(bvid)
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
            
            # 4. 计算基础业务指标
            timestamps = [v['pub_timestamp'] for v in all_videos_data]
            publish_std = self.business_layer.calculate_publish_std(timestamps)
            triple_rate_std = self.business_layer.calculate_triple_rates(all_videos_data)
            
            # 5. DS模型稳定性评估
            stability_result = self.business_layer.evaluate_up_stability(timestamps, all_videos_data)
            stability_report = self.business_layer.generate_stability_report(stability_result, up_name)
            
            # 6. 互动水平分析
            user_metrics = self.interaction_analyzer.analyze_interaction_level(all_videos_data)
            interaction_report = self.interaction_analyzer.generate_interaction_report(user_metrics, up_name)
            
            # 7. 保存数据
            ds_data = {
                "metadata": {
                    "uid": str(uid),
                    "up_name": up_name,
                    "data_created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "video_count": len(all_videos_data),
                    "publish_std_seconds": publish_std,
                    "triple_rate_std": triple_rate_std,
                    "stability_analysis": stability_result,
                    "interaction_metrics": user_metrics
                },
                "videos": all_videos_data
            }
            
            def save_operation():
                os.makedirs(f"{self.data_dir}/ups", exist_ok=True)
                filename = f"{self.data_dir}/ups/{uid}.json"
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(ds_data, f, ensure_ascii=False, indent=2)
                return filename
            
            filename = self.infra.file_operation("保存数据文件", save_operation)
            
            print(f"✅ DS模型数据已保存至: {filename}")
            print(f"📊 包含 {len(all_videos_data)} 个视频数据")
            
            # 8. 显示分析报告
            print(stability_report)
            print(interaction_report)
            
            # 9. 显示性能报告
            self.presentation.display_performance_report()
            
            return True
            
        except Exception as e:
            print(f"❌ 导出失败: {e}")
            return False
        
    async def analyze_up_stability(self, uid):
        """仅分析UP主稳定性（不保存数据）"""
        print(f"🔄 正在分析UP主 {uid} 的运营稳定性...")
        
        try:
            # 1. 获取用户信息
            user_info = await self.data_layer.get_user_info(uid)
            up_name = user_info['name']
            
            # 2. 获取视频列表
            videos_response = await self.data_layer.get_user_videos(uid)
            video_list = videos_response['list']['vlist'] if videos_response else []
            
            # 3. 批量获取视频详情（只取最近20个视频以提高速度）
            recent_videos = video_list[:20]
            all_videos_data = []
            
            for video_item in recent_videos:
                bvid = video_item['bvid']
                video_detail = await self.data_layer.get_video_data(bvid)
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
            stability_result = self.business_layer.evaluate_up_stability(timestamps, all_videos_data)
            stability_report = self.business_layer.generate_stability_report(stability_result, up_name)
            
            # 5. 显示稳定性报告
            print(stability_report)
            
            return True
            
        except Exception as e:
            print(f"❌ 分析失败: {e}")
            return False

    async def analyze_up_interaction(self, uid):
        """分析UP主互动水平"""
        print(f"🔄 正在分析UP主 {uid} 的互动水平...")
        
        try:
            # 1. 获取用户信息
            user_info = await self.data_layer.get_user_info(uid)
            up_name = user_info['name']
            
            # 2. 获取视频列表
            videos_response = await self.data_layer.get_user_videos(uid)
            video_list = videos_response['list']['vlist'] if videos_response else []
            
            # 3. 批量获取视频详情（最近15个）
            recent_videos = video_list[:15]
            all_videos_data = []
            
            for video_item in recent_videos:
                bvid = video_item['bvid']
                video_detail = await self.data_layer.get_video_data(bvid)
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
            
        except Exception as e:
            print(f"❌ 互动分析失败: {e}")
            return False

    async def comprehensive_analysis(self, uid):
        """综合分析：稳定性 + 互动水平"""
        print(f"🔄 正在对UP主 {uid} 进行综合分析...")
        
        try:
            # 1. 获取用户信息
            user_info = await self.data_layer.get_user_info(uid)
            up_name = user_info['name']
            
            # 2. 获取视频列表
            videos_response = await self.data_layer.get_user_videos(uid)
            video_list = videos_response['list']['vlist'] if videos_response else []
            
            # 3. 批量获取视频详情（最近20个）
            recent_videos = video_list[:20]
            all_videos_data = []
            
            for video_item in recent_videos:
                bvid = video_item['bvid']
                video_detail = await self.data_layer.get_video_data(bvid)
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
            stability_result = self.business_layer.evaluate_up_stability(timestamps, all_videos_data)
            stability_report = self.business_layer.generate_stability_report(stability_result, up_name)
            
            # 5. 互动水平分析
            user_metrics = self.interaction_analyzer.analyze_interaction_level(all_videos_data)
            interaction_report = self.interaction_analyzer.generate_interaction_report(user_metrics, up_name)
            
            # 6. 显示完整报告
            print("🎯 UP主综合分析报告")
            print("=" * 60)
            print(stability_report)
            print(interaction_report)
            
            return True
            
        except Exception as e:
            print(f"❌ 综合分析失败: {e}")
            return False