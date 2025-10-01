#!/usr/bin/env python3
"""
B站视频数据分析 - 终极精简版
输入BV号，获取三连数据并生成柱状图
"""

import asyncio
import matplotlib.pyplot as plt
from bilibili_api import video

class BilibiliQuickAnalyzer:
    def __init__(self):
        plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
        plt.rcParams['axes.unicode_minus'] = False
    
    async def get_video_data(self, bvid):
        """获取视频数据"""
        try:
            v = video.Video(bvid=bvid)
            info = await v.get_info()
            return info
        except Exception as e:
            print(f"❌ 获取视频失败: {e}")
            return None
    
    def analyze_and_plot(self, bvid):
        """分析并绘图 - 主函数"""
        print(f"🎯 正在分析视频: {bvid}")
        
        # 获取数据
        info = asyncio.run(self.get_video_data(bvid))
        if not info:
            return
        
        # 提取关键数据
        stat = info['stat']
        data = {
            '标题': info['title'][:20] + '...' if len(info['title']) > 20 else info['title'],
            '播放量': stat['view'],
            '点赞数': stat['like'], 
            '投币数': stat['coin'],
            '收藏数': stat['favorite']
        }
        
        # 打印结果
        print(f"\n📊 分析结果:")
        print(f"标题: {info['title']}")
        print(f"UP主: {info['owner']['name']}")
        print(f"播放量: {data['播放量']:,}")
        print(f"点赞数: {data['点赞数']:,}")
        print(f"投币数: {data['投币数']:,}") 
        print(f"收藏数: {data['收藏数']:,}")
        
        # 计算比率
        total = data['点赞数'] + data['投币数'] + data['收藏数']
        print(f"三连总数: {total:,}")
        print(f"点赞率: {data['点赞数']/data['播放量']:.2%}")
        print(f"投币率: {data['投币数']/data['播放量']:.2%}")
        print(f"收藏率: {data['收藏数']/data['播放量']:.2%}")
        
        # 生成柱状图
        self.generate_bar_chart(data, bvid)
    
    def generate_bar_chart(self, data, bvid):
        """生成三连数据柱状图"""
        labels = ['播放量', '点赞数', '投币数', '收藏数']
        values = [data['播放量'], data['点赞数'], data['投币数'], data['收藏数']]
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728']
        
        plt.figure(figsize=(10, 6))
        bars = plt.bar(labels, values, color=colors, alpha=0.7)
        
        # 设置图表样式
        plt.title(f'B站视频数据分析\n{data["标题"]}\nBV: {bvid}', fontsize=14)
        plt.ylabel('数量')
        
        # 在柱子上显示数值
        for bar, value in zip(bars, values):
            plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(values)*0.01, 
                    f'{value:,}', ha='center', va='bottom', fontweight='bold')
        
        plt.grid(axis='y', alpha=0.3)
        plt.tight_layout()
        plt.show()

# 使用示例
if __name__ == "__main__":
    analyzer = BilibiliQuickAnalyzer()
    
    # 直接在这里输入BV号！
    bv_id = "BV1cSnuzYE88"  # 🔥 修改这里的BV号！
    
    analyzer.analyze_and_plot(bv_id)