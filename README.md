# Daily Tech News 生成系统

> 整合 V2EX、Hacker News、科技媒体 RSS，每日自动化生成科技简报.


## 是什么

一个全自动的科技新闻聚合与简报生成系统，每天自动抓取技术社区热点，通过 AI 分析整理成结构化简报。

### 核心价值

本系统具备省时、智能、全面、自动化等特点：你无需手动浏览多个网站，每天只需查看一份简报即可掌握科技动态；系统通过 AI 自动筛选热点、提炼趋势、生成摘要；内容覆盖中文社区、国际资讯、科技媒体等多个维度；每天定时生成简报，并自动推送到仓库，无需人工干预。

### 简报示例

每日简报包含三大板块：

```
1. 今日必读 - 当天最重要/最值得关注的要点
2. 趋势与解读 - 从新闻中提炼趋势，并给出简短解读
3. 工具与深读 - 开源项目、开发工具、教程/长文精选
```

## 为什么

### 解决的问题

| 痛点 | 解决方案 |
|------|----------|
| 信息分散，需要浏览 10+ 个网站 | 整合 V2EX、HN、RSS 等多个数据源 |
| 内容太多，没时间细看 | AI 筛选精华，生成精简中文简报 |
| 缺乏上下文，不知道什么重要 | AI 分析重要性，标注趋势 |
| 需要收藏和归档 | 自动保存 Markdown + HTML 格式 |

### 适用场景

- **开发者**：快速了解技术趋势、热门项目
- **产品经理**：获取行业动态、竞品信息
- **创业者**：关注投资风向、创业资讯
- **学生**：拓展技术视野、学习前沿知识

## 使用方式

### 方式一：直接查看（推荐）

如果已配置 GitHub Pages，访问你的 Pages 地址查看最新简报，无需任何配置。

### 方式二：本地运行

```bash
# 进入项目目录
cd daily-tech-news

# 安装依赖（推荐使用 uv，速度更快）
# 方式一：使用 uv（推荐）
curl -LsSf https://astral.sh/uv/install.sh | sh  # 首次安装 uv
uv pip install -r requirements.txt

# 方式二：使用传统 pip
python -m pip install -r requirements.txt

# 配置 API Key
# 方式一：使用 .env 文件（推荐，本地开发）
# 在项目根目录创建 .env 文件，内容如下：
# ANTHROPIC_API_KEY=your-siliconflow-api-key
# ANTHROPIC_BASE_URL=https://api.siliconflow.cn/v1

# 方式二：使用环境变量
export ANTHROPIC_API_KEY="your-siliconflow-api-key"
export ANTHROPIC_BASE_URL="https://api.siliconflow.cn/v1"

# 运行生成
python scripts/tech_digest.py

# 生成 HTML 页面
python scripts/generate_page.py  # 生成每日详情页
python scripts/generate_html.py  # 生成首页列表

# 查看生成的简报
cat digests/latest.md

# 本地预览（可选）
python -m http.server 8000
# 然后访问 http://localhost:8000
```

### 方式三：使用 GitHub Actions 自动化

1. **配置 GitHub Secrets**：在仓库设置中添加 `ANTHROPIC_API_KEY`（你的 SiliconFlow API Key）
2. **启用 GitHub Actions**（默认已启用）
3. **确认定时任务已启用**：访问仓库的 Actions 页面，确保工作流处于启用状态
4. **等待每天 8:10（北京时间）自动生成**

**手动触发**：除了定时运行，你也可以在 GitHub Actions 页面点击 "Run workflow" 按钮随时手动触发生成。

**失败重试**：如果某次运行失败，可以在失败的运行记录页面点击 "Re-run jobs" 按钮重新执行。

**定时任务不运行？** 请查看下方的"定时任务故障排除"章节。

如需自定义，可修改配置文件：

| 文件 | 用途 |
|------|------|
| `scripts/config.json` | RSS 源、模型配置 |
| `.github/workflows/daily-tech-digest.yml` | 定时任务配置 |

## 项目结构

```
daily-tech-news/
├── .github/workflows/        # GitHub Actions 配置
│   └── daily-tech-digest.yml
├── scripts/                  # 核心脚本
│   ├── tech_digest.py        # 主脚本（数据抓取 + AI 生成）
│   ├── generate_html.py      # 生成首页列表（index.html）
│   ├── generate_page.py      # 生成每日详情页（digests/YYYY-MM-DD.html）
│   ├── siliconflow_client.py # SiliconFlow API 封装
│   ├── config.json           # 配置文件
│   └── use_agent_sdk.py      # Agent SDK 使用示例（已弃用）
├── digests/                  # 简报输出目录
│   ├── 2026-01-22.md         # 每日 Markdown 简报
│   ├── 2026-01-22.html       # 每日 HTML 详情页
│   ├── 2026-01-22.sources.json # 原始数据备份
│   └── latest.md             # 最新简报（符号链接）
├── index.html                # 首页列表（所有简报的入口）
├── requirements.txt          # Python 依赖
├── .env                      # 本地环境变量（需自行创建，已加入 .gitignore）
└── README.md
```

### 网站结构

- **首页 (`index.html`)**：显示最新 10 条简报，按日期倒序排列，并提供分页导航
- **分页 (`page-2.html` 等)**：展示更早的简报列表（每页 10 条）
- **详情页 (`digests/YYYY-MM-DD.html`)**：点击列表项进入，显示当天的完整简报内容

## 配置说明

### 数据源

当前配置的数据源（可在 `scripts/config.json` 修改）：

| 类别 | 来源 | 数量 |
|------|------|------|
| 技术社区 | V2EX 热门话题 | 20 条 |
| 国际资讯 | Hacker News Top | 20 条 |
| 科技媒体 | 36氪、少数派、虎嗅、InfoQ、开源中国、Solidot | 60 条 |

### AI 配置

使用 SiliconFlow 的 Anthropic 兼容 API：

**本地开发**：推荐使用 `.env` 文件（已在 `.gitignore` 中，不会被提交）
```bash
# 在项目根目录创建 .env 文件
ANTHROPIC_API_KEY=your-siliconflow-api-key
ANTHROPIC_BASE_URL=https://api.siliconflow.cn/v1
```

**GitHub Actions**：在仓库 Settings → Secrets 中配置 `ANTHROPIC_API_KEY`

**模型配置**（`scripts/config.json`）：
```json
{
  "llm": {
    "model": "zai-org/GLM-5.2",
    "max_tokens": 2200,
    "base_url": "https://api.siliconflow.cn/v1",
    "timeout_seconds": 120,
    "retries": 3
  }
}
```

**输出截断应对**（默认配置已启用）：
- 输出结构收敛为 3 个板块，降低总长度
- 每个板块条目数受 `digest.min_items_per_section / max_items_per_section` 限制（默认 4-5）
- 每条摘要建议控制在 150 字以内（`build_prompt()` 中约束）
- 若仍截断，可适当提高 `llm.max_tokens` 或继续压缩条目/摘要

### 定时任务

GitHub Actions 默认配置：每天北京时间 8:10 运行

```yaml
schedule:
  - cron: '10 0 * * *'  # UTC 00:10 = 北京 8:10
```

## 工作原理

```
┌─────────────────┐
│  定时触发        │
│  (每天 8:10)     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  数据抓取        │
│  • V2EX API     │
│  • HN Firebase  │
│  • RSS 源       │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  AI 分析生成     │
│  • 筛选热点      │
│  • 提炼趋势      │
│  • 生成摘要      │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  保存与发布      │
│  • Markdown     │
│  • HTML         │
│  • Git 提交      │
└─────────────────┘
```

## 开发指南

### 添加新的 RSS 源

编辑 `scripts/config.json`，在 `sources.rss.feeds` 数组中添加：

```json
{
  "sources": {
    "rss": {
      "feeds": [
        {
          "id": "new-source",
          "name": "新来源",
          "url": "https://example.com/feed",
          "category": "tech"
        }
      ]
    }
  }
}
```

### 修改简报结构

编辑 `scripts/tech_digest.py` 中的 `build_prompt` 函数，调整 AI 输出格式和结构。

### 自定义样式

- **首页列表样式**：编辑 `scripts/generate_html.py` 中的 `INDEX_TEMPLATE` CSS
- **详情页样式**：编辑 `scripts/generate_page.py` 中的 `HTML_TEMPLATE` CSS

### 手动重新生成

如果 AI 生成失败，可以在 GitHub Actions 中点击 "Re-run jobs" 按钮手动重试。也可以使用 `workflow_dispatch` 触发器随时手动运行。

## 定时任务故障排除

如果定时任务没有自动运行，请按以下步骤排查：

### 1. 确认工作流已启用

1. 访问仓库的 **Actions** 标签页
2. 在左侧找到 **Daily Tech Digest** 工作流
3. 如果看到黄色横幅提示"Workflows aren't being run on this repository"，点击 **"I understand my workflows, go ahead and enable them"** 按钮启用

### 2. 检查工作流状态

1. 在 Actions 页面，确认 **Daily Tech Digest** 工作流旁边没有显示 "disabled" 标记
2. 如果显示 disabled，点击工作流名称，然后点击 **"Enable workflow"** 按钮

### 3. GitHub 定时任务的已知限制

- **延迟**：GitHub Actions 的定时任务可能会有 10-30 分钟的延迟，特别是在高峰期
- **60 天规则**：如果仓库超过 60 天没有活动，GitHub 会自动禁用定时任务。本仓库已配置 keep-alive 工作流来防止这种情况
- **新仓库**：新创建的仓库可能需要手动在 Actions 页面确认启用工作流

### 4. 验证定时任务配置

定时任务使用 cron 表达式 `10 0 * * *`（UTC），即北京时间每天 8:10 运行。

### 5. 查看运行历史

在 Actions 页面可以查看所有运行记录。如果定时任务正常运行，应该能看到 event 为 "schedule" 的运行记录。
