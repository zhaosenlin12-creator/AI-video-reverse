# AI四小只 数据抓取工具

> 这层负责把抖音 / 小红书真实数据抓回来，给 ai-douyin-pipeline skill 用。

## 一次性安装

1. 启动 Chrome 远程调试模式（首次）：
   ```
   双击 start_chrome.bat
   ```
   - 自动检测 Chrome 安装路径
   - 启动 chrome 远程调试端口 9222
   - 保持窗口打开

2. 第一次跑爬虫会弹抖音二维码，用你日常登录抖音的手机扫码。

## 三个 .bat 入口

### run_crawler.bat
抓 AI四小只 抖音账号数据（creator 主页）。
输出 data/creator/contents.jsonl + comments.jsonl。

### run_hotlist.bat
抓抖音 "AI工具,AI编程,WorkBuddy,AI Agent" 关键词搜索结果 Top 50。
输出 data/hotlist/contents.jsonl。

### run_xhs_hotlist.bat
抓小红书 "AI工具,AI编程,WorkBuddy,提示词" 关键词搜索结果 Top 50。
输出 data/hotlist_xhs/contents.jsonl。

## 与 ai-douyin-pipeline skill 集成

调用 skill 时：
- Stage 0 自动跑 scripts/fetch_account_metrics.py
- Stage 2 自动跑 scripts/fetch_hotlist.py dy
- 抓回来的数据自动进 history.md / hotlist.json

## 手动跑（调试用）

从 skill 目录或 tools 目录都能跑：

```
# 抓账号
python scripts/fetch_account_metrics.py

# 只解析已有 jsonl（不跑爬虫）
python scripts/fetch_account_metrics.py --parse

# 抓抖音热榜
python scripts/fetch_hotlist.py dy

# 抓小红书热榜
python scripts/fetch_hotlist.py xhs

# 都抓
python scripts/fetch_hotlist.py both
```

## 数据落盘

```
tools/
├── MediaCrawler/                    # 仓库本体
├── data/
│   ├── creator/                     # AI四小只 账号数据
│   │   ├── contents.jsonl           # 视频列表
│   │   ├── comments.jsonl           # 评论
│   │   └── creators.jsonl           # 创作者信息
│   ├── hotlist/                     # 抖音热榜
│   │   └── contents.jsonl
│   └── hotlist_xhs/                 # 小红书热榜
│       └── contents.jsonl
├── hotlist.json                     # 汇总热榜（Stage 2 用）
├── start_chrome.bat                 # 启动 Chrome 远程调试
├── run_crawler.bat                  # 抓账号
├── run_hotlist.bat                  # 抓抖音热榜
└── run_xhs_hotlist.bat              # 抓小红书热榜
```

## 注意事项

- Chrome 必须保持打开状态
- 第一次跑需要扫码登录抖音
- MediaCrawler 默认并发数 1，每条数据间隔 2 秒（避免风控）
- 不要连续高频抓（一天 1-2 次足够）
- 抓完可以关闭 Chrome 窗口（下次开需重扫码）

## 已知边界

- 未登录的抖音视频拿不到完整数据，必须扫码登录
- 抖音风控强，频繁抓可能被临时封号（建议每天最多抓 3 次）
- 抓取的数据只能用于学习 / 研究 / 自己的账号分析，不能二次分发
