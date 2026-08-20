# AI 视频逆向工作流

> 一个**数据驱动 + 权重自调**的短视频脚本自动生成系统。
> 用 MediaCrawler 抓自己账号的真实互动数据，**复制自己历史爆款**的视频脚本。

## 这是什么

抖音 / 小红书账号做内容时最大的痛点是：**不知道下一个爆款长什么样**。

本工作流的做法：

1. 用 [MediaCrawler](https://github.com/NanmiCoder/MediaCrawler) 抓账号历史视频的真实互动数据（点赞、收藏、评论、分享）
2. 按互动分排名找出**历史爆款**，拆解它们的特征（钩子、主体、收尾、关键词）
3. 每次需要新脚本时，按"爆款特征匹配度"打分选题，让新视频朝历史赢家偏移
4. 每 4 周自动回测，调维度权重，让爆款率逐步上升

## 5 分钟快速开始

### 1. 克隆 + 装依赖

```
git clone https://github.com/zhaosen林12-creator/AI-video-reverse.git
cd AI-video-reverse

# 装 MediaCrawler 依赖
cd tools/MediaCrawler
pip install -r requirements.txt
playwright install chromium
cd ../..

# 装你自己的脚本依赖
pip install requests jieba
```

### 2. 配置账号

复制配置模板：

```
cp config.example.json config.json
```

编辑 `config.json`，填入你的抖音 sec_uid（在创作者主页 URL 里）。

### 3. 启动 Chrome + 抓数据

```
# 启动 Chrome 远程调试模式
tools/start_chrome.bat

# 第一次跑：浏览器里手动登录抖音
# 跑抓账号数据
python scripts/fetch_account_metrics.py
```

### 4. 出脚本

用 [Codex](https://codex.openai.com) 加载这个项目，然后说"出脚本"：

```
@codex 出脚本
```

Codex 会自动调 ai-douyin-pipeline skill，按"历史爆款特征"生成 3 条带"预期播放档位"的脚本。

完整文档见 [WORKFLOW.md](WORKFLOW.md)。

## 适用对象

- 想稳定产出爆款的个人 / 团队账号
- 已经积累 ≥5 条视频的账号（有历史数据可回测）
- 用 Codex / 类似 AI agent 的用户

## 不适用

- 全新账号（0 历史数据，回测无依据）
- 不愿用 AI 工具的纯人工运营

## 工作原理

```
你的抖音账号
  ↓ MediaCrawler + CDP + Chrome
tools/data/creator/*.jsonl
  ↓ fetch_account_metrics.py
references/account-history.md（互动分排名）
  ↓ tune_weights.py（每 4 周）
references/weight-tuning.md（维度权重）
  ↓ Codex ai-douyin-pipeline skill
video/<YYYY>-Wxx>/*.md（3 条带预期档位的脚本）
```

## 项目结构

```
AI-video-reverse/
├── README.md                # 你正在读这个
├── WORKFLOW.md              # 完整工作流教程
├── workflow.md              # 旧版工作流文档
├── config.example.json      # 配置模板
├── config.json              # 你的配置（git ignore）
├── .gitignore               # 敏感文件排除
├── LICENSE
├── tools/
│   ├── README.md            # 抓取工具说明
│   ├── start_chrome.bat     # 启动 Chrome 远程调试
│   ├── run_crawler.bat      # 抓账号数据
│   ├── run_hotlist.bat      # 抓抖音热榜
│   ├── run_xhs_hotlist.bat  # 抓小红书热榜
│   └── MediaCrawler/        # git submodule（clone 时自动拉）
├── scripts/
│   ├── fetch_account_metrics.py  # 抓账号 + 写 history
│   ├── fetch_hotlist.py          # 抓热榜 + 汇总 JSON
│   ├── update_history.py         # 手动更新播放数据
│   └── tune_weights.py           # 4 周回测调权重
├── references/              # 历史数据 + 权重 + 模板
│   ├── account-history.md   # 历史视频互动数据
│   ├── weight-tuning.md     # 当前维度权重
│   ├── script-blueprint.md  # 5 种脚本骨架
│   └── algorithm-bounds.md  # 算法边界声明
└── video/                   # 已发布的脚本（按周归档）
    └── 2026-W34/
        ├── 01-workbuddy-getting-started.md
        ├── 02-workbuddy-vs-openclaw.md
        └── 03-workbuddy-5sentences-prompt.md
```

## 自定义到适合你的工作流

这个工作流可以适配**任何短视频账号**，不只是 AI 教学类：

1. **改账号画像**（`references/account-profile.md`）—— 受众、调性、赛道
2. **改脚本模板**（`references/script-blueprint.md`）—— 你的视频结构
3. **改打分维度**（`references/weight-tuning.md`）—— 你的爆款特征
4. **改关键词库**（`tools/run_hotlist.bat`）—— 你赛道的热点关键词

完整自定义指南见 [WORKFLOW.md § 自定义](WORKFLOW.md#自定义到适合你的工作流)。

## 边界声明

⚠️ **没有任何算法能 100% 预测爆款**。我们做的是：

1. 复制你自己历史爆款的特征
2. 按数据排序新选题
3. 让爆款率从"随缘"变成"模式化"

实际命中率取决于账号权重、拍摄质量、发布节奏。完整说明见 [references/algorithm-bounds.md](references/algorithm-bounds.md)。

## 贡献

欢迎 PR 改进：

- 新平台的抓取适配
- 新的打分维度
- 新的脚本骨架类型
- 真实的回测案例

## 许可证

[MIT](LICENSE)
