#!/usr/bin/env python3
"""
互动分析模块
基于收集的基准数据提供互动水平分析
"""

import json
import numpy as np

class InteractionAnalyzer:
    """互动水平分析器"""
    
    def __init__(self, benchmark_file="bilibili_growth_reference.json"):
        self.benchmarks = self.load_benchmarks(benchmark_file)
    
    def load_benchmarks(self, benchmark_file):
        """加载基准数据"""
        try:
            with open(benchmark_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            # 返回默认基准（基于我们之前分析的数据）
            return {
                "startup_benchmarks": {
                    "engagement_standards": {
                        "like_rate_benchmark": 0.0436,
                        "coin_rate_benchmark": 0.0101,
                        "good_performance_threshold": 0.0499
                    }
                },
                "current_benchmarks": {
                    "engagement_standards": {
                        "like_rate_benchmark": 0.0439,
                        "coin_rate_benchmark": 0.0075,
                        "good_performance_threshold": 0.0552
                    }
                }
            }
    
    def analyze_interaction_level(self, user_videos):
        """分析用户互动水平"""
        if not user_videos:
            return None
        
        # 计算用户互动指标
        views = [v['view'] for v in user_videos]
        likes = [v['like'] for v in user_videos]
        coins = [v['coin'] for v in user_videos]
        favorites = [v['favorite'] for v in user_videos]
        danmakus = [v.get('danmaku', 0) for v in user_videos]
        replies = [v.get('reply', 0) for v in user_videos]
        
        # 计算互动率
        like_rates = [like/view for like, view in zip(likes, views) if view > 0]
        coin_rates = [coin/view for coin, view in zip(coins, views) if view > 0]
        favorite_rates = [fav/view for fav, view in zip(favorites, views) if view > 0]
        danmaku_densities = [dan/view*60 for dan, view in zip(danmakus, views) if view > 0]  # 条/分钟
        comment_rates = [reply/view for reply, view in zip(replies, views) if view > 0]
        
        user_metrics = {
            "like_rate": np.mean(like_rates) if like_rates else 0,
            "coin_rate": np.mean(coin_rates) if coin_rates else 0,
            "favorite_rate": np.mean(favorite_rates) if favorite_rates else 0,
            "danmaku_density": np.mean(danmaku_densities) if danmaku_densities else 0,
            "comment_rate": np.mean(comment_rates) if comment_rates else 0,
            "video_count": len(user_videos),
            "avg_views": np.mean(views) if views else 0
        }
        
        return user_metrics
    
    def generate_interaction_report(self, user_metrics, up_name):
        """生成互动分析报告"""
        startup_bench = self.benchmarks["startup_benchmarks"]["engagement_standards"]
        current_bench = self.benchmarks["current_benchmarks"]["engagement_standards"]
        
        report = []
        report.append(f"\n🎯 UP主【{up_name}】互动水平分析报告")
        report.append("══════════════════════════════════════")
        
        # 基础定位
        report.append(f"📊 基础定位")
        report.append(f"   视频数量: {user_metrics['video_count']} 个")
        report.append(f"   平均播放: {user_metrics['avg_views']:,.0f}")
        
        # 判断成长阶段
        if user_metrics['avg_views'] < 100000:
            stage = "探索期新人"
        elif user_metrics['avg_views'] < 500000:
            stage = "成长期UP主"
        else:
            stage = "稳定期创作者"
        report.append(f"   成长阶段: {stage}")
        
        report.append(f"\n💬 互动水平分析")
        
        # 点赞率分析
        like_score = self._evaluate_metric(
            user_metrics['like_rate'], 
            startup_bench['like_rate_benchmark'],
            current_bench['like_rate_benchmark']
        )
        report.append(f"👍 点赞率: {user_metrics['like_rate']*100:.1f}% {like_score['emoji']}")
        report.append(f"   {like_score['bar']}")
        report.append(f"   行业基准: 新人{startup_bench['like_rate_benchmark']*100:.1f}% → 成熟{current_bench['like_rate_benchmark']*100:.1f}%")
        
        # 投币率分析
        coin_score = self._evaluate_metric(
            user_metrics['coin_rate'],
            startup_bench['coin_rate_benchmark'],
            current_bench['coin_rate_benchmark']
        )
        report.append(f"🪙 投币率: {user_metrics['coin_rate']*100:.1f}% {coin_score['emoji']}")
        report.append(f"   {coin_score['bar']}")
        report.append(f"   行业基准: 新人{startup_bench['coin_rate_benchmark']*100:.1f}% → 成熟{current_bench['coin_rate_benchmark']*100:.1f}%")
        
        # 弹幕密度分析
        danmaku_bench = 5.0  # 条/分钟基准
        danmaku_score = self._evaluate_danmaku(user_metrics['danmaku_density'], danmaku_bench)
        report.append(f"💬 弹幕密度: {user_metrics['danmaku_density']:.1f}条/分钟 {danmaku_score['emoji']}")
        report.append(f"   {danmaku_score['bar']}")
        report.append(f"   活跃基准: >{danmaku_bench}条/分钟")
        
        # 改进建议
        report.append(f"\n💡 立即改进建议")
        suggestions = self._generate_suggestions(user_metrics, startup_bench)
        for i, suggestion in enumerate(suggestions[:3], 1):
            report.append(f"   {i}. {suggestion}")
        
        return "\n".join(report)
    
    def _evaluate_metric(self, user_value, startup_bench, current_bench):
        """评估单个指标"""
        if user_value >= current_bench:
            score = 1.0
            emoji = "🏆"
        elif user_value >= startup_bench:
            score = (user_value - startup_bench) / (current_bench - startup_bench)
            emoji = "⭐"
        else:
            score = user_value / startup_bench
            emoji = "💡"
        
        bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
        return {"score": score, "bar": bar, "emoji": emoji}
    
    def _evaluate_danmaku(self, density, bench):
        """评估弹幕密度"""
        if density >= bench * 2:
            score = 1.0
            emoji = "🏆"
        elif density >= bench:
            score = 0.5 + (density - bench) / bench * 0.5
            emoji = "⭐"
        else:
            score = density / bench
            emoji = "💡"
        
        bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
        return {"score": score, "bar": bar, "emoji": emoji}
    
    def _generate_suggestions(self, user_metrics, startup_bench):
        """生成改进建议"""
        suggestions = []
        
        # 点赞率建议
        if user_metrics['like_rate'] < startup_bench['like_rate_benchmark']:
            suggestions.append("优化片尾设计，明确引导点赞")
        
        # 投币率建议  
        if user_metrics['coin_rate'] < startup_bench['coin_rate_benchmark']:
            suggestions.append("增强内容稀缺性，提升投币价值")
        
        # 弹幕密度建议
        if user_metrics['danmaku_density'] < 3:
            suggestions.append("增加视频中的互动话题点")
        
        # 通用建议
        if len(suggestions) < 3:
            suggestions.extend([
                "保持稳定更新频率，培养粉丝习惯",
                "分析高互动视频，复制成功模式",
                "加强评论区互动，提升粉丝粘性"
            ])
        
        return suggestions[:3]