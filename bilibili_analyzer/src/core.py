
"""
B站视频分析核心模块
"""
import asyncio
import time
from bilibili_api import video

class BilibiliAnalyzer:
    """B站视频分析器"""

    def __init__(self):
        self.sequence = []
        self.start_time = time.time()

    def _checkpoint(self, step_name):
        """内部断点检查"""
        timestamp = time.time() - self.start_time
        self.sequence.append(1)
        print(f"⏰ [{timestamp:.3f}s] {step_name}: 1")
        return timestamp

    async def analyze_video(self, bv_id):
        """分析视频数据"""
        try:
            # 创建视频对象
            self._checkpoint("创建视频对象")
            v = video.Video(bvid=bv_id)

            # 获取视频信息
            self._checkpoint("获取API数据")
            info = await v.get_info()

            # 提取数据
            self._checkpoint("解析数据")
            title = info['title']
            up_name = info['owner']['name']
            stat = info['stat']

            # 整理结果
            result = {
                'bv_id': bv_id,
                'title': title,
                'up_name': up_name,
                'view': stat['view'],
                'like': stat['like'],
                'coin': stat['coin'],
                'favorite': stat['favorite'],
                'share': stat['share'],
                'reply': stat['reply'],
                'sequence': self.sequence.copy(),
                'total_time': time.time() - self.start_time
            }

            # 计算比率
            result['like_rate'] = result['like'] / result['view']
            result['coin_rate'] = result['coin'] / result['view']
            result['favorite_rate'] = result['favorite'] / result['view']

            self._checkpoint("分析完成")
            return result

        except Exception as e:
            print(f"❌ 分析失败: {e}")
            return None

class InteractiveTester:
    """交互式测试器"""

    def __init__(self):
        self.analyzer = BilibiliAnalyzer()

    async def run_interactive_test(self):
        """运行交互式测试"""
        while True:
            print("\n" + "="*50)
            bv_id = input("请输入BV号 (输入 'q' 退出): ").strip()

            if bv_id.lower() == 'q':
                print("测试结束！")
                break

            if not bv_id.startswith('BV'):
                print("❌ 请输入有效的BV号")
                continue

            print(f"🎯 正在分析: {bv_id}")
            result = await self.analyzer.analyze_video(bv_id)

            if result:
                self._display_result(result)
            else:
                print("❌ 分析失败")

    def _display_result(self, result):
        """显示分析结果"""
        print(f"\n✅ 分析成功!")
        print(f"📺 标题: {result['title']}")
        print(f"👤 UP主: {result['up_name']}")
        print(f"📊 播放量: {result['view']:,}")
        print(f"👍 点赞: {result['like']:,} ({result['like_rate']:.2%})")
        print(f"🪙 投币: {result['coin']:,} ({result['coin_rate']:.2%})")
        print(f"⭐ 收藏: {result['favorite']:,} ({result['favorite_rate']:.2%})")
        print(f"🔢 执行序列: {''.join(str(x) for x in result['sequence'])}")
        print(f"⏱️  总耗时: {result['total_time']:.3f}s")
