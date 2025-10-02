



```markdown
# B站视频分析器 (Bilibili Analyzer)

**版本**: v2.0.0  
**最后更新**: 2024年（当前日期）

## 🚀 功能特性

### v2.0.0 新增功能
✅ **双视频对比分析** - 支持同时分析两个BV号并进行数据对比  
✅ **完整数据统计** - 评论数、点赞数、投币数、收藏数、分享数、弹幕数  
✅ **智能图表展示** - 对比柱状图 + 比率分析图  
✅ **项目规范化** - 完整的.gitignore配置，依赖管理

### 基础功能
✅ 单视频数据分析  
✅ 交互式终端输入  
✅ 数据可视化图表  
✅ 比率计算分析

## 📊 数据指标

- 📺 播放量
- 👍 点赞数  
- 🪙 投币数
- ⭐ 收藏数
- 💬 评论数
- 📤 分享数
- 🎯 弹幕数
- 📈 各项数据比率分析

## 🛠️ 安装使用

### 环境要求
- Python 3.7+
- 依赖包见 `requirements.txt`

### 快速开始
```bash
# 克隆项目
git clone https://github.com/xjswantoffwork/bilibli_analyzer.git

# 安装依赖
pip install -r requirements.txt

# 运行分析器
python main.py
```

### 使用示例
```bash
🎬 B站视频对比分析工具
==================================================
📝 请输入两个BV号进行对比分析
请输入第一个BV号: BV1cSnuzYE88
请输入第二个BV号: BV1Jx4y1a7uL
```

## 📁 项目结构

```
bilibli_analyzer/
├── main.py                 # 主程序 - 对比分析功能
├── requirements.txt        # Python依赖包
├── .gitignore             # Git忽略配置
└── README.md              # 项目说明
```

## 🔧 依赖包

```txt
bilibili-api-python>=10.4.0
requests>=2.28.0
beautifulsoup4>=4.11.0
pandas>=1.5.0
matplotlib>=3.6.0
asyncio
```

## 📈 版本历史

### v2.0.0 (当前)
- 新增双视频对比功能
- 添加完整数据统计指标
- 项目配置规范化
- 增强图表可视化

### v1.0.0 
- 基础单视频分析功能
- 基础数据可视化
- 项目初始化

## 🎯 开发计划

- [ ] Web界面开发
- [ ] 数据导出功能
- [ ] 批量分析功能
- [ ] 历史记录管理

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

MIT License

---
**开发者**: xjswantoffwork  
**仓库**: https://github.com/xjswantoffwork/bilibli_analyzer
```

## 🎯 这个README的特点：

### ✅ **版本管理**
- 清晰的版本号 v2.0.0
- 版本历史记录
- 功能更新说明

### ✅ **专业结构**
- 功能特性列表
- 安装使用指南
- 项目结构说明
- 开发计划

### ✅ **用户友好**
- 使用示例
- 可视化emoji
- 清晰的代码块

## 📝 更新README：

```bash
# 替换现有的README.md
# 然后提交更新
git add README.md
git commit -m "docs: 更新README.md，添加v2.0.0版本说明"
git push origin master
```
