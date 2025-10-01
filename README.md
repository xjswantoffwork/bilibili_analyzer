
# B站数据分析工具

一个用于分析B站视频数据的Python工具。

## 功能
- 视频数据获取和分析
- 用户信息统计
- 数据可视化
- 弹幕数据分析

## 安装
```bash
pip install requests pandas matplotlib jupyter
```

## 使用
```python
from bilibili_analyzer import BilibiliAnalyzer

analyzer = BilibiliAnalyzer()
data = analyzer.get_video_data("BV号")
```

## 运行
```bash
python bilibili_analyzer.py
```

## 项目结构
- `bilibili_analyzer.py` - 主程序
- `bilibili_analyzer/` - 包目录
- `bilibili_analyzer.ipynb` - Notebook示例
```

**直接复制上面的整个代码块**，然后在 GitHub 仓库页面：
1. 点击 "Add file" → "Create new file"
2. 文件名输入 `README.md`
3. 粘贴复制的内容
4. 点击 "Commit new file"

或者在你的本地项目中使用：
```bash
# 将内容保存到 README.md 文件
# 然后执行：
git add README.md
git commit -m "docs: add README.md"
git push origin master
```
