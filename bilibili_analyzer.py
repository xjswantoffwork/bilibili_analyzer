#!/usr/bin/env python3
"""
B站视频数据分析 -
在终端中输入两个BV号，进行对比分析并生成对比柱状图
"""

import asyncio
import matplotlib.pyplot as plt
import numpy as np
from bilibili_api import video

class BilibiliCompareAnalyzer:
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
            print(f"❌ 获取视频 {bvid} 失败: {e}")
            return None

    def get_video_stats(self, info, bvid):
        """提取视频统计数据"""
        if not info:
            return None
            
        stat = info['stat']
        return {
            'BV号': bvid,
            '标题': info['title'][:25] + '...' if len(info['title']) > 25 else info['title'],
            '完整标题': info['title'],
            'UP主': info['owner']['name'],
            '播放量': stat['view'],
            '点赞数': stat['like'], 
            '投币数': stat['coin'],
            '收藏数': stat['favorite'],
            '评论数': stat['reply'],
            '分享数': stat['share'],
            '弹幕数': stat['danmaku']
        }
    
    def print_comparison(self, data1, data2):
        """打印对比结果"""
        print(f"\n📊 视频对比分析结果:")
        print("=" * 80)
        
        # 视频1信息
        print(f"🎬 视频1 - {data1['BV号']}:")
        print(f"   标题: {data1['完整标题']}")
        print(f"   UP主: {data1['UP主']}")
        print(f"   播放量: {data1['播放量']:,}")
        print(f"   点赞数: {data1['点赞数']:,} | 投币数: {data1['投币数']:,} | 收藏数: {data1['收藏数']:,}")
        print(f"   评论数: {data1['评论数']:,} | 分享数: {data1['分享数']:,} | 弹幕数: {data1['弹幕数']:,}")
        
        # 视频2信息
        print(f"\n🎬 视频2 - {data2['BV号']}:")
        print(f"   标题: {data2['完整标题']}")
        print(f"   UP主: {data2['UP主']}")
        print(f"   播放量: {data2['播放量']:,}")
        print(f"   点赞数: {data2['点赞数']:,} | 投币数: {data2['投币数']:,} | 收藏数: {data2['收藏数']:,}")
        print(f"   评论数: {data2['评论数']:,} | 分享数: {data2['分享数']:,} | 弹幕数: {data2['弹幕数']:,}")
        
        # 对比分析
        print(f"\n📈 数据对比:")
        self.print_difference("播放量", data1['播放量'], data2['播放量'])
        self.print_difference("点赞数", data1['点赞数'], data2['点赞数'])
        self.print_difference("投币数", data1['投币数'], data2['投币数'])
        self.print_difference("收藏数", data1['收藏数'], data2['收藏数'])
        self.print_difference("评论数", data1['评论数'], data2['评论数'])
        
        # 比率对比
        print(f"\n📊 比率对比:")
        self.print_ratio_comparison("点赞率", data1['点赞数'], data1['播放量'], data2['点赞数'], data2['播放量'])
        self.print_ratio_comparison("投币率", data1['投币数'], data1['播放量'], data2['投币数'], data2['播放量'])
        self.print_ratio_comparison("收藏率", data1['收藏数'], data1['播放量'], data2['收藏数'], data2['播放量'])
        self.print_ratio_comparison("评论率", data1['评论数'], data1['播放量'], data2['评论数'], data2['播放量'])

    def print_difference(self, metric, value1, value2):
        """打印数值差异"""
        diff = value1 - value2
        if diff > 0:
            print(f"   {metric}: 视频1比视频2多 {abs(diff):,} ({diff/value2:+.1%})")
        elif diff < 0:
            print(f"   {metric}: 视频1比视频2少 {abs(diff):,} ({diff/value1:+.1%})")
        else:
            print(f"   {metric}: 两者相同")

    def print_ratio_comparison(self, metric, num1, den1, num2, den2):
        """打印比率对比"""
        ratio1 = num1 / den1 if den1 > 0 else 0
        ratio2 = num2 / den2 if den2 > 0 else 0
        diff = ratio1 - ratio2
        
        if diff > 0:
            status = "更高"
        elif diff < 0:
            status = "更低"
        else:
            status = "相同"
            
        print(f"   {metric}: 视频1 {ratio1:.2%} vs 视频2 {ratio2:.2%} (视频1{status})")

    def generate_comparison_chart(self, data1, data2):
        """生成对比柱状图"""
        # 设置对比数据
        metrics = ['点赞数', '投币数', '收藏数', '评论数', '分享数', '弹幕数']
        values1 = [data1['点赞数'], data1['投币数'], data1['收藏数'], 
                  data1['评论数'], data1['分享数'], data1['弹幕数']]
        values2 = [data2['点赞数'], data2['投币数'], data2['收藏数'], 
                  data2['评论数'], data2['分享数'], data2['弹幕数']]
        
        # 创建分组柱状图
        x = np.arange(len(metrics))
        width = 0.35
        
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        
        # 第一个图：互动数据对比
        bars1 = ax1.bar(x - width/2, values1, width, label=data1['标题'], alpha=0.7, color='#1f77b4')
        bars2 = ax1.bar(x + width/2, values2, width, label=data2['标题'], alpha=0.7, color='#ff7f0e')
        
        ax1.set_title('B站视频数据对比分析', fontsize=16, fontweight='bold', pad=20)
        ax1.set_ylabel('数量', fontsize=12)
        ax1.set_xticks(x)
        ax1.set_xticklabels(metrics, rotation=45)
        ax1.legend()
        ax1.grid(axis='y', alpha=0.3)
        
        # 在柱子上显示数值
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax1.text(bar.get_x() + bar.get_width()/2., height + max(max(values1), max(values2))*0.01,
                        f'{int(height):,}', ha='center', va='bottom', fontsize=9)
        
        # 第二个图：比率对比
        ratios1 = [
            data1['点赞数'] / data1['播放量'],
            data1['投币数'] / data1['播放量'], 
            data1['收藏数'] / data1['播放量'],
            data1['评论数'] / data1['播放量']
        ]
        ratios2 = [
            data2['点赞数'] / data2['播放量'],
            data2['投币数'] / data2['播放量'],
            data2['收藏数'] / data2['播放量'], 
            data2['评论数'] / data2['播放量']
        ]
        ratio_metrics = ['点赞率', '投币率', '收藏率', '评论率']
        
        x_ratio = np.arange(len(ratio_metrics))
        bars3 = ax2.bar(x_ratio - width/2, ratios1, width, label=data1['标题'], alpha=0.7, color='#1f77b4')
        bars4 = ax2.bar(x_ratio + width/2, ratios2, width, label=data2['标题'], alpha=0.7, color='#ff7f0e')
        
        ax2.set_title('数据比率对比', fontsize=14, fontweight='bold', pad=20)
        ax2.set_ylabel('比率', fontsize=12)
        ax2.set_xticks(x_ratio)
        ax2.set_xticklabels(ratio_metrics)
        ax2.legend()
        ax2.grid(axis='y', alpha=0.3)
        
        # 在比率柱子上显示百分比
        for bars in [bars3, bars4]:
            for bar in bars:
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height + 0.001,
                        f'{height:.2%}', ha='center', va='bottom', fontsize=9)
        
        # 添加总体信息
        plt.figtext(0.5, 0.01, 
                   f"视频1播放量: {data1['播放量']:,} | 视频2播放量: {data2['播放量']:,} | "
                   f"视频1UP主: {data1['UP主']} | 视频2UP主: {data2['UP主']}", 
                   ha='center', fontsize=10, style='italic')
        
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.1)
        plt.show()

    async def compare_videos(self, bv1, bv2):
        """比较两个视频"""
        print(f"🔄 正在获取视频数据...")
        print(f"   视频1: {bv1}")
        print(f"   视频2: {bv2}")
        
        # 异步获取两个视频数据
        task1 = self.get_video_data(bv1)
        task2 = self.get_video_data(bv2)
        results = await asyncio.gather(task1, task2)
        
        data1 = self.get_video_stats(results[0], bv1)
        data2 = self.get_video_stats(results[1], bv2)
        
        if not data1 or not data2:
            print("❌ 至少有一个视频数据获取失败，请检查BV号是否正确")
            return False
        
        # 打印对比结果
        self.print_comparison(data1, data2)
        
        # 生成对比图表
        self.generate_comparison_chart(data1, data2)
        
        return True

def main():
    """主函数 - 支持两个BV号对比"""
    analyzer = BilibiliCompareAnalyzer()
    
    print("🎬 B站视频对比分析工具")
    print("=" * 50)
    
    while True:
        try:
            print("\n📝 请输入两个BV号进行对比分析")
            bv1 = input("请输入第一个BV号: ").strip()
            
            if bv1.lower() == 'q':
                print("👋 感谢使用，再见！")
                break
            
            bv2 = input("请输入第二个BV号: ").strip()
            
            if bv2.lower() == 'q':
                print("👋 感谢使用，再见！")
                break
            
            # 验证BV号格式
            if not (bv1.startswith('BV') and bv2.startswith('BV')):
                print("❌ 请输入正确的BV号，以 'BV' 开头")
                continue
            
            # 执行对比分析
            asyncio.run(analyzer.compare_videos(bv1, bv2))
            
            print("\n" + "=" * 50)
            
        except KeyboardInterrupt:
            print("\n\n👋 用户中断，感谢使用！")
            break
        except Exception as e:
            print(f"❌ 发生错误: {e}")
            continue

if __name__ == "__main__":
    main()