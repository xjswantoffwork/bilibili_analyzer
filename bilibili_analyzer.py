#!/usr/bin/env python3
"""
B站视频数据分析 - 带性能监控的版本
"""

import numpy as np
import asyncio
import json
import os
import time
from datetime import datetime
from bilibili_api import video, user

################################################################################
# ========== 1. 性能监控层 ==========
################################################################################
class PerformanceMonitor:
    """专门负责性能数据收集和分析"""
    
    def __init__(self):
        self.performance_data = []
        self.current_operation = None
        self.operation_start_time = None
        
    def start_operation(self, operation_name, operation_type):
        """开始监控一个操作"""
        self.current_operation = operation_name
        self.operation_start_time = time.time()
        
    def end_operation(self, success=True):
        """结束当前操作的监控"""
        if self.current_operation and self.operation_start_time:
            duration = time.time() - self.operation_start_time
            
            self.performance_data.append({
                "operation": self.current_operation,
                "duration": round(duration, 3),  # 保留3位小数
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "success": success
            })
            
            # 重置
            self.current_operation = None
            self.operation_start_time = None
    
    def get_performance_report(self):
        """生成性能分析报告"""
        if not self.performance_data:
            return "暂无性能数据"
        
        # 按操作类型分类统计
        network_ops = [op for op in self.performance_data if "get_" in op["operation"]]
        file_ops = [op for op in self.performance_data if "save_" in op["operation"]]
        data_ops = [op for op in self.performance_data if "calculate_" in op["operation"]]
        display_ops = [op for op in self.performance_data if "display_" in op["operation"]]
        
        report = []
        report.append("🔍 性能分析报告：")
        report.append("══════════════════════════════════════")
        
        # 网络请求统计
        if network_ops:
            total_network = sum(op["duration"] for op in network_ops)
            report.append(f"📡 网络请求 (总耗时: {total_network:.1f}秒)")
            for op in network_ops:
                report.append(f"  ├─ {op['operation']}: {op['duration']}秒")
        
        # 文件操作统计
        if file_ops:
            total_file = sum(op["duration"] for op in file_ops)
            report.append(f"💾 文件操作 (总耗时: {total_file:.1f}秒)")
            for op in file_ops:
                report.append(f"  ├─ {op['operation']}: {op['duration']}秒")
        
        # 数据处理统计
        if data_ops:
            total_data = sum(op["duration"] for op in data_ops)
            report.append(f"⚡ 数据处理 (总耗时: {total_data:.1f}秒)")
            for op in data_ops:
                report.append(f"  ├─ {op['operation']}: {op['duration']}秒")
        
        # 显示操作统计
        if display_ops:
            total_display = sum(op["duration"] for op in display_ops)
            report.append(f"📊 显示输出 (总耗时: {total_display:.1f}秒)")
            for op in display_ops:
                report.append(f"  ├─ {op['operation']}: {op['duration']}秒")
        
        # 总结
        total_time = sum(op["duration"] for op in self.performance_data)
        if total_time > 0:
            network_percent = (total_network / total_time * 100) if network_ops else 0
            report.append(f"📈 总结: 总共{total_time:.1f}秒，网络请求占{network_percent:.1f}%")
        
        return "\n".join(report)
    
    def clear_data(self):
        """清空性能数据"""
        self.performance_data = []

################################################################################
# ========== 2. 基础设施层（网络、文件IO） ==========
################################################################################
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

################################################################################
# ========== 3. 数据层（数据获取、格式化） ==========
################################################################################
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

################################################################################
# ========== 4. 业务层（分析逻辑、算法） ==========
################################################################################
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

################################################################################
# ========== 5. 表现层（用户界面、显示） ==========
################################################################################
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
            # ... 其他显示逻辑
            
            self.monitor.end_operation(True)
        except Exception as e:
            self.monitor.end_operation(False)
            raise e
    
    def display_performance_report(self):
        """显示性能报告"""
        self.monitor.start_operation("display_performance", "display")
        print(f"\n{self.monitor.get_performance_report()}")
        self.monitor.end_operation(True)

################################################################################
# ========== 6. 控制层（流程协调、调度） ==========
################################################################################
class BilibiliVideoAnalyzer:
    """主控制器 - 协调各层工作"""
    
    def __init__(self):
        # 初始化各层
        self.monitor = PerformanceMonitor()
        self.infra = InfrastructureLayer(self.monitor)
        self.data_layer = DataLayer(self.infra, self.monitor)
        self.business_layer = BusinessLayer(self.monitor)
        self.presentation = PresentationLayer(self.monitor)
        
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
                        "favorite": video_detail['stat']['favorite']
                    }
                    all_videos_data.append(video_data)
            
            # 4. 计算业务指标
            timestamps = [v['pub_timestamp'] for v in all_videos_data]
            publish_std = self.business_layer.calculate_publish_std(timestamps)
            triple_rate_std = self.business_layer.calculate_triple_rates(all_videos_data)
            
            # 5. 保存数据
            ds_data = {
                "metadata": {
                    "uid": str(uid),
                    "up_name": up_name,
                    "data_created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "video_count": len(all_videos_data),
                    "publish_std_seconds": publish_std,
                    "triple_rate_std": triple_rate_std
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
            
            # 6. 显示性能报告
            self.presentation.display_performance_report()
            
            return True
            
        except Exception as e:
            print(f"❌ 导出失败: {e}")
            return False
        
################################################################################
# ========== 主程序分区 ==========
################################################################################
def main():
    """主函数"""
    analyzer = BilibiliVideoAnalyzer()
    
    print("🎬 B站视频分析工具 - 性能监控版")
    print("=" * 50)
    
    while True:
        try:
            print("\n📝 请选择模式:")
            print("1. UP主数据导出 (输入UID)")
            print("2. 查看性能报告")
            print("3. 清空性能数据")
            print("4. 退出")
            
            choice = input("请选择模式 (1/2/3/4): ").strip()
            
            if choice == '4':
                print("👋 感谢使用，再见！")
                break
            elif choice == '1':
                uid = input("请输入UP主UID: ").strip()
                if not uid.isdigit():
                    print("❌ UID应为数字")
                    continue
                
                analyzer.monitor.clear_data()
                success = asyncio.run(analyzer.export_up_data(uid))
                
            elif choice == '2':
                analyzer.presentation.display_performance_report()
                
            elif choice == '3':
                analyzer.monitor.clear_data()
                print("✅ 性能数据已清空")
                
            else:
                print("❌ 请输入 1, 2, 3 或 4")
                continue
            
            print("=" * 50)
            
        except KeyboardInterrupt:
            print("\n\n👋 用户中断，感谢使用！")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            continue

if __name__ == "__main__":
    main()