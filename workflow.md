# 完整工作流教程

> 5 分钟快速开始见 [README.md](README.md)。
> 本文是**完整版**，讲清楚每一层的原理和怎么自定义。

## 工作流总览

```
┌─────────────────────────────────────────────────────┐
│  你的账号（抖音 / 小红书 / 视频号）                │
└────────────────────┬────────────────────────────────┘
                     │ MediaCrawler + CDP
                     ↓
┌─────────────────────────────────────────────────────┐
│  数据抓取层                                          │
│  • fetch_account_metrics.py → tools/data/creator/  │
│  • fetch_hotlist.py → tools/hotlist.json            │
└────────────────────┬────────────────────────────────┘
                     │ 解析 JSONL
                     ↓
┌─────────────────────────────────────────────────────┐
│  历史数据层                                          │
│  • references/account-history.md（视频互动分排名）  │
│  • references/weight-tuning.md（维度权重）          │
└────────────────────┬────────────────────────────────┘
                     │ Codex 加载
                     ↓
┌─────────────────────────────────────────────────────┐
│  Codex skill: ai-douyin-pipeline                    │
│  7 阶段流水线：                                       │
│   Stage 0 数据回收 → 1 准备 → 2 扫热点 → 3 打分   │
│   → 4 出脚本 → 5 保存 → 6 写回 → 7 回测            │
└────────────────────┬────────────────────────────────┘
                     │ 输出
                     ↓
┌─────────────────────────────────────────────────────┐
│  视频脚本（按周归档）                                │
│  video/2026-Wxx/*.md（带预期播放档位）              │
└─────────────────────────────────────────────────────┘
```

## 安装详解

### 系统要求

- Windows 10+ / macOS / Linux
- Python 3.11+（MediaCrawler 测试用 3.12）
- Google Chrome（用于远程调试）
- [Codex](https://codex.openai.com) 或类似 AI agent
- Git

### 步骤 1：拉仓库

```
git clone https://github.com/zhaosen林12-creator/AI-video-reverse.git
cd AI-video-reverse
git submodule update --init   # 拉 MediaCrawler
```

MediaCrawler 是 git submodule（避免污染主仓库）。

### 步骤 2：装 Python 依赖

```
# MediaCrawler 依赖（多，约 30 个包）
cd tools/MediaCrawler
pip install -r requirements.txt

# Playwright 浏览器
playwright install chromium
cd ../..

# 项目自己的脚本依赖
pip install requests jieba
```

国内用户建议加清华源：

```
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```

### 步骤 3：配置账号

```
cp config.example.json config.json
```

打开 `config.json`，填入：

- `account.douyin_sec_uid` —— 你的抖音 sec_uid
  获取：访问抖音创作者主页 URL，例如
  `https://www.douyin.com/user/MS4wLjABAAAA...`
  `MS4wLjABAAAA...` 就是 sec_uid
- `account.douyin_handle` —— 你的抖音号（@后面的名字）
- `platforms` —— 启用哪些平台
- `schedule` —— 抓取频率

### 步骤 4：第一次抓数据

#### 4.1 启动 Chrome 远程调试

**Windows：**

```
# 双击运行 tools/start_chrome.bat
# 或手动跑：
"C:\Program Files\Google\Chrome\Application\chrome.exe" --remote-debugging-port=9222
```

**macOS：**

```
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222
```

**Linux：**

```
google-chrome --remote-debugging-port=9222
```

Chrome 启动后，**保持窗口开着**。MediaCrawler 会通过 9222 端口连接它。

#### 4.2 浏览器里登录抖音

在刚启动的 Chrome 里：

1. 访问 https://www.douyin.com/
2. 点击登录，扫码确认
3. 登录态会缓存到 Chrome user-data-dir

> ⚠️ 用你**自己的抖音账号**登录，**不是 AI 视频里那个角色账号**——抖音 API 对非创作者本人访问不返回 video_play_count。

#### 4.3 跑抓账号脚本

```
python scripts/fetch_account_metrics.py
```

这会：
1. 通过 CDP 连接 Chrome 9222 端口
2. 调 MediaCrawler 抓你账号的所有视频
3. 输出 `tools/data/creator/creator_contents_<日期>.jsonl`
4. 自动追加日志到 `references/account-history.md`

首次抓约需 1-2 分钟（每视频间隔 2 秒，避免风控）。

### 步骤 5：在 Codex 里加载项目

把项目目录告诉 Codex：

```
@codex 加载项目 C:\path\to\AI-video-reverse
```

Codex 会自动识别 `references/` 下的文件作为 skill 上下文。

或者把 skill 安装到 Codex：

```
# 把 scripts/ 和 references/ 复制到 Codex skill 目录
cp -r scripts/ ~/...codex/skills/ai-douyin-pipeline/
cp -r references/ ~/...codex/skills/ai-douyin-pipeline/
```

### 步骤 6：出脚本

在 Codex 对话框里说：

```
出脚本
```

或者：

```
跑一次 skill
```

Codex 会自动跑 7 阶段流水线（Stage 0-7），输出 3 条带"预期档位"的脚本到 `video/<当前周>/`。

## 自定义到适合你的工作流

这个工作流**不绑定任何特定赛道**。按下面 4 步定制：

### Step A：改账号画像

编辑 `references/account-profile.md`：

```
# 基础信息
- 抖音昵称：你的账号名
- 签名：你的简介
- 粉丝 / 获赞：当前数据

# 调性
- 受众：你的目标观众
- 风格：教学 / 搞笑 / 测评 / ...
- 必备元素：每条视频必须有什么

# 赛道
- 核心：你主要做的内容
- 避开：不做什么

# 拍摄条件
- 你的机位 / 设备 / 人员
```

### Step B：改脚本模板

编辑 `references/script-blueprint.md`，把"知识库爆款原版"换成你账号的真实爆款逐秒拆解：

```
| 秒 | 主体 | 字幕 | 镜头 |
|---|---|---|---|
| 0.0 | 你的角色 | 你的开场标题 | 封面 |
| 1.0 | ... | ... | ... |
```

### Step C：改打分维度

编辑 `references/weight-tuning.md`，按你的赛道调维度权重。
比如你的赛道是"搞笑段子"，可以：

- 拍摄可行性 +1（段子好拍）
- 上升趋势 -1（段子时效性弱）
- 爆款特征匹配 +1（直接复制你自己的段子结构）

### Step D：改关键词库

编辑 `tools/run_hotlist.bat`，把关键词换成你赛道的：

```
--keywords "搞笑段子,网络梗,娱乐新闻"
```

## 进阶：调权重逻辑

工作流会**自动**调权重，但你也可以手动调：

### 什么时候跑 tune_weights.py

- 每 4 周自动跑（脚本里写好了）
- 你觉得最近视频流量明显下降时
- 你换了一个新赛道时

### 跑法

```
python scripts/tune_weights.py
```

它会：
1. 读 `references/account-history.md` 近 4 周数据
2. 按视频类型算平均互动分
3. 按规则自动调权重（写入 `weight-tuning.md`）
4. 打印调权建议

### 调权规则

- 某类型平均互动分 > 500 → 该类型对应的维度 +1
- 某类型平均互动分 < 100 且样本 ≥ 2 → 该类型对应的维度 -1
- 实测型平均 < 100 → 爆款特征匹配 +1

## 常见问题

### Q：为什么 video_play_count 是 0？

A：抖音 API 对非创作者本人访问不返回播放数据。用点赞 / 收藏 / 评论 / 分享作为代理。

完整说明见 [algorithm-bounds.md](references/algorithm-bounds.md)。

### Q：抓数据时被抖音风控怎么办？

A：
1. 减少抓取频率（每天 ≤ 3 次）
2. 错开抓取时间
3. 暂停 24-48 小时

### Q：怎么验证 MediaCrawler 在跑？

A：
1. 检查 Chrome 是否打开（要有窗口）
2. 浏览器访问 http://127.0.0.1:9222/json/version —— 应该返回 Chrome 元数据
3. 检查 `tools/data/creator/` 目录是否有新 jsonl

### Q：submodule 拉不下来？

A：
1. 检查网络（可能需要 VPN）
2. 直接 `git clone https://github.com/NanmiCoder/MediaCrawler.git tools/MediaCrawler/`

### Q：换平台怎么改？

A：MediaCrawler 支持抖音 / 小红书 / 快手 / B站 / 微博 / 贴吧 / 知乎。改 `tools/run_hotlist.bat` 的 `--platform` 参数：

```
--platform xhs    # 小红书
--platform bili   # B 站
--platform wb     # 微博
```

## 路线图

- [ ] 支持自动生成封面图
- [ ] 支持视频剪辑自动化
- [ ] 支持多账号管理
- [ ] Web UI（自动跑工作流 + 看数据看板）

## 反馈

提 issue：https://github.com/zhaosen林12-creator/AI-video-reverse/issues
