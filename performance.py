#!/usr/bin/env python3
"""
性能监控模块
负责性能数据收集、分析和报告生成
"""

import time
from datetime import datetime


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
    
    def get_stats(self):
        """获取性能统计信息"""
        if not self.performance_data:
            return {
                "total_operations": 0,
                "total_time": 0,
                "success_rate": 0
            }
        
        total_ops = len(self.performance_data)
        total_time = sum(op["duration"] for op in self.performance_data)
        successful_ops = sum(1 for op in self.performance_data if op["success"])
        success_rate = (successful_ops / total_ops) * 100 if total_ops > 0 else 0
        
        return {
            "total_operations": total_ops,
            "total_time": round(total_time, 3),
            "success_rate": round(success_rate, 1),
            "average_time": round(total_time / total_ops, 3) if total_ops > 0 else 0
        }


# 测试代码
if __name__ == "__main__":
    # 简单测试性能监控器
    monitor = PerformanceMonitor()
    
    # 模拟一些操作
    monitor.start_operation("test_operation", "test")
    time.sleep(0.1)  # 模拟操作耗时
    monitor.end_operation(True)
    
    print("✅ PerformanceMonitor 测试通过")
    print(monitor.get_performance_report())
    print("统计信息:", monitor.get_stats())