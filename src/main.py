# src/main.py
"""
主程序入口
"""

import asyncio
import sys
import os

# 添加当前目录到Python路径
current_dir = os.path.dirname(__file__)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from core.analyzer import BilibiliVideoAnalyzer

async def main():
    """主函数"""
    if len(sys.argv) < 3:
        print("用法: python main.py <命令> <UID>")
        print("命令:")
        print("  export    导出UP主完整数据")
        print("  stability 分析运营稳定性")
        print("  interaction 分析互动水平")
        print("  comprehensive 综合分析")
        return
    
    command = sys.argv[1].lower()
    uid = int(sys.argv[2])
    
    analyzer = BilibiliVideoAnalyzer()
    
    try:
        if command == "export":
            await analyzer.export_up_data(uid)
        elif command == "stability":
            await analyzer.analyze_up_stability(uid)
        elif command == "interaction":
            await analyzer.analyze_up_interaction(uid)
        elif command == "comprehensive":
            await analyzer.comprehensive_analysis(uid)
        else:
            print(f"未知命令: {command}")
            
    except KeyboardInterrupt:
        print("\n👋 用户中断操作")
    except Exception as e:
        print(f"❌ 程序执行出错: {e}")

if __name__ == "__main__":
    asyncio.run(main())