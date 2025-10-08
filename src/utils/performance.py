# src/utils/performance.py
"""
性能监控模块
"""

import time
from datetime import datetime
from typing import List, Dict, Any, Optional

class PerformanceMonitor:
    """性能监控器"""
    
    def __init__(self):
        self.performance_data: List[Dict[str, Any]] = []
        self.current_operation: Optional[str] = None
        self.operation_start_time: Optional[float] = None
        
    def start_operation(self, operation_name: str, operation_type: str):
        """开始监控一个操作"""
        self.current_operation = operation_name
        self.operation_start_time = time.time()
        
    def end_operation(self, success: bool = True):
        """结束当前操作的监控"""
        if self.current_operation and self.operation_start_time:
            duration = time.time() - self.operation_start_time
            
            self.performance_data.append({
                "operation": self.current_operation,
                "duration": round(duration, 3),
                "timestamp": datetime.now().strftime("%H:%M:%S"),
                "success": success
            })
            
            # 重置状态
            self.current_operation = None
            self.operation_start_time = None
    
    def get_performance_report(self) -> str:
        """生成性能分析报告"""
        if not self.performance_data:
            return "暂无性能数据"
        
        report = []
        report.append("🔍 性能分析报告：")
        report.append("══════════════════════════════════════")
        
        total_time = sum(op["duration"] for op in self.performance_data)
        
        for op in self.performance_data:
            status = "✅" if op["success"] else "❌"
            report.append(f"  {status} {op['operation']}: {op['duration']}秒")
        
        report.append(f"📈 总耗时: {total_time:.1f}秒")
        
        return "\n".join(report)
    
    def clear_data(self):
        """清空性能数据"""
        self.performance_data = []