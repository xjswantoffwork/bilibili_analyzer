# run.py
import sys
import os
import asyncio

# 添加src目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

# 现在直接导入并运行核心功能
try:
    # 直接在这里实现核心功能，避免复杂的导入
    from bilibili_api import video, user
    import numpy as np
    import json
    from datetime import datetime
    
    class SimpleAnalyzer:
        def __init__(self):
            self.performance_data = []
        
        async def analyze_stability(self, uid):
            print(f"🔄 正在分析UP主 {uid} 的运营稳定性...")
            
            try:
                # 1. 获取用户信息
                print("📡 获取用户信息...")
                user_obj = user.User(uid=uid)
                user_info = await user_obj.get_user_info()
                up_name = user_info['name']
                print(f"✅ 获取到UP主: {up_name}")
                
                # 2. 获取视频列表
                print("📡 获取视频列表...")
                videos_data = await user_obj.get_videos()
                video_list = videos_data.get('list', {}).get('vlist', [])
                
                if not video_list:
                    print("❌ 该UP主没有视频或视频列表为空")
                    return False
                
                print(f"✅ 获取到 {len(video_list)} 个视频")
                
                # 3. 分析最近8个视频
                recent_videos = video_list[:8]
                all_videos_data = []
                
                for i, video_item in enumerate(recent_videos, 1):
                    print(f"📊 分析视频 {i}/{len(recent_videos)}: {video_item['title'][:20]}...")
                    bvid = video_item['bvid']
                    
                    try:
                        video_obj = video.Video(bvid=bvid)
                        video_detail = await video_obj.get_info()
                        
                        video_data = {
                            "bvid": bvid,
                            "pub_timestamp": video_detail['pubdate'],
                            "view": video_detail['stat']['view'],
                            "like": video_detail['stat']['like'],
                            "coin": video_detail['stat']['coin'],
                            "favorite": video_detail['stat']['favorite']
                        }
                        all_videos_data.append(video_data)
                    except Exception as e:
                        print(f"⚠️ 跳过视频 {bvid}: {e}")
                        continue
                
                # 4. 计算稳定性
                if len(all_videos_data) < 2:
                    print("❌ 视频数量不足，无法进行稳定性分析")
                    return False
                
                # 时间稳定性分析
                timestamps = [v['pub_timestamp'] for v in all_videos_data]
                intervals = np.diff(sorted(timestamps))
                time_std = np.std(intervals)
                avg_interval = np.mean(intervals)
                time_stability = 1 / (1 + time_std / max(avg_interval, 24*3600))
                
                # 质量稳定性分析
                triple_rates = []
                for v in all_videos_data:
                    if v['view'] > 0:
                        rate = (v['like'] + v['coin'] + v['favorite']) / v['view']
                        triple_rates.append(rate)
                
                if triple_rates:
                    quality_std = np.std(triple_rates)
                    quality_avg = np.mean(triple_rates)
                    quality_stability = 1 / (1 + quality_std / quality_avg) if quality_avg > 0 else 0.5
                else:
                    quality_stability = 0.5
                
                # 综合稳定性
                overall_stability = time_stability * 0.6 + quality_stability * 0.4
                
                # 5. 生成报告
                print(f"\n📊 UP主【{up_name}】运营稳定性报告")
                print("══════════════════════════════════════")
                
                # 时间稳定性
                time_bar = "█" * int(time_stability * 20) + "░" * (20 - int(time_stability * 20))
                print(f"⏰ 时间稳定性: {time_stability*100:.1f}%")
                print(f"   {time_bar}")
                
                # 质量稳定性
                quality_bar = "█" * int(quality_stability * 20) + "░" * (20 - int(quality_stability * 20))
                print(f"⭐ 质量稳定性: {quality_stability*100:.1f}%")
                print(f"   {quality_bar}")
                
                # 综合评估
                overall_bar = "█" * int(overall_stability * 20) + "░" * (20 - int(overall_stability * 20))
                if overall_stability >= 0.8:
                    level = "优秀 🏆"
                elif overall_stability >= 0.6:
                    level = "良好 ⭐"
                elif overall_stability >= 0.4:
                    level = "一般 📊"
                else:
                    level = "待提升 💡"
                
                print(f"🏆 综合稳定性: {overall_stability*100:.1f}% ({level})")
                print(f"   {overall_bar}")
                
                # 分析建议
                print(f"\n💡 分析建议:")
                if overall_stability >= 0.8:
                    print("   ✅ 运营非常稳定，具备专业UP主特征")
                    print("   💡 建议：继续保持高质量的规律更新")
                elif overall_stability >= 0.6:
                    print("   👍 运营较为稳定，有良好的内容规划")
                    print("   💡 建议：优化发布时间规律性")
                elif overall_stability >= 0.4:
                    print("   📈 运营基本稳定，有提升空间")
                    print("   💡 建议：加强内容质量一致性")
                else:
                    print("   🔄 运营波动较大，建议系统规划")
                    print("   💡 建议：建立固定的更新节奏")
                
                print(f"\n📈 基于 {len(all_videos_data)} 个视频数据分析")
                return True
                
            except Exception as e:
                print(f"❌ 分析失败: {e}")
                import traceback
                traceback.print_exc()
                return False
    
    async def main():
        if len(sys.argv) < 3:
            print("用法: python run.py <命令> <UID>")
            print("命令: stability, interaction, comprehensive, export")
            return
        
        command = sys.argv[1].lower()
        uid = int(sys.argv[2])
        
        analyzer = SimpleAnalyzer()
        
        if command == "stability":
            await analyzer.analyze_stability(uid)
        else:
            print(f"命令 {command} 暂未实现，目前只支持 stability")
    
    if __name__ == "__main__":
        asyncio.run(main())
        
except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("请确保已安装依赖: pip install bilibili-api-python numpy")