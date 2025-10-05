#!/usr/bin/env python3
"""
B站视频数据分析 - 主程序入口
"""

import asyncio
from analysis import BilibiliVideoAnalyzer

def main():
    """主函数"""
    analyzer = BilibiliVideoAnalyzer()
    
    print("🎬 B站UP主分析工具 - 专业版")
    print("=" * 50)
    
    while True:
        try:
            print("\n📝 请选择分析模式:")
            print("1. UP主数据导出 (完整分析 + 保存数据)")
            print("2. UP主稳定性分析 (快速模式)")
            print("3. UP主互动水平分析")
            print("4. UP主综合分析 (稳定性 + 互动)")
            print("5. 查看性能报告")
            print("6. 清空性能数据")
            print("7. 退出")
            
            choice = input("请选择模式 (1-7): ").strip()
            
            if choice == '7':
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
                uid = input("请输入UP主UID: ").strip()
                if not uid.isdigit():
                    print("❌ UID应为数字")
                    continue
                
                analyzer.monitor.clear_data()
                success = asyncio.run(analyzer.analyze_up_stability(uid))
                
            elif choice == '3':
                uid = input("请输入UP主UID: ").strip()
                if not uid.isdigit():
                    print("❌ UID应为数字")
                    continue
                
                analyzer.monitor.clear_data()
                success = asyncio.run(analyzer.analyze_up_interaction(uid))
                
            elif choice == '4':
                uid = input("请输入UP主UID: ").strip()
                if not uid.isdigit():
                    print("❌ UID应为数字")
                    continue
                
                analyzer.monitor.clear_data()
                success = asyncio.run(analyzer.comprehensive_analysis(uid))
                
            elif choice == '5':
                analyzer.presentation.display_performance_report()
                
            elif choice == '6':
                analyzer.monitor.clear_data()
                print("✅ 性能数据已清空")
                
            else:
                print("❌ 请输入 1-7 的数字")
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