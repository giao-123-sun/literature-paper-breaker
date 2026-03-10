# Literature Paper Breaker (LPB) — 项目完整文档

> 首个专为人文社科设计的AI论文研究引擎 — 从文献检索到完整论文，全流程自动化
>
> The first AI research pipeline built specifically for humanities & social sciences

---

## 目录

1. [项目概述](#1-项目概述)
2. [系统架构](#2-系统架构)
3. [核心模块详解](#3-核心模块详解)
4. [LLM 多模型策略](#4-llm-多模型策略)
5. [图片生成能力](#5-图片生成能力gemini-31-flash)
6. [安装与配置](#6-安装与配置)
7. [使用指南](#7-使用指南)
8. [数据源详解](#8-数据源详解)
9. [输出格式与文件结构](#9-输出格式与文件结构)
10. [开发指南](#10-开发指南)
11. [成本估算](#11-成本估算)
12. [推广计划摘要](#12-推广计划摘要)

---

## 1. 项目概述

### 1.1 定位

Literature Paper Breaker (LPB) 是一个 AI 驱动的人文社科学术研究自动化系统。与市面上所有竞品（gpt_academic、AI-Scientist、GPT-Researcher 等）面向理工科/通用领域不同，LPB **专为人文社科研究设计**，支持解释性（humanities）和假说驱动（social science）两种研究范式。

### 1.2 核心差异点

| 特性 | LPB | 竞品 |
|------|-----|------|
| **学科定位** | 人文社科专精 | 理工科/通用 |
| **数据诚信** | 区分"可计算完成" vs "需要人工调研"，不编造数据 | 常伪造调研数据和统计 |
| **全流程自动化** | 文献检索→综述→空白分析→假说→大纲→写作→同行评审 | 大多只覆盖部分环节 |
| **多数据库整合** | OpenAlex + Semantic Scholar + CrossRef + CORE + CText | 通常单一来源 |
| **中英文双语** | 原生支持中文研究，含中国古典文献库 | 英文优先 |
| **多模型策略** | 支持 Anthropic/OpenAI/OpenRouter，可混用大小模型 | 通常绑定单一模型 |

### 1.3 支持学科

Economics, History, Political Science, Sociology, Philosophy, Literature, Linguistics, Anthropology, Law, Education, Psychology, Art History, Religious Studies, Area Studies

---

## 2. 系统架构

### 2.1 Pipeline 总览

```
[研究主题输入]
       │
       ▼
┌──────────────────┐
│  Literature Search │ ← OpenAlex / Semantic Scholar / CrossRef / CORE / CText
│  (多源并行检索+去重) │
└──────────┬───────┘
           ▼
┌──────────────────┐
│ Literature Review  │ ← LLM 分析主题、趋势、方法论
│ (系统性文献综述)    │
└──────────┬───────┘
           ▼
┌──────────────────┐
│   Gap Analysis     │ ← 识别理论盲区、方法缺陷、矛盾发现
│  (研究空白分析)     │
└──────────┬───────┘
           ▼
┌──────────────────┐
│ Hypothesis Gen     │ ← 提出原创研究问题/可检验假说
│ (假说/问题生成)     │
└──────────┬───────┘
           ▼
┌──────────────────┐
│  Paper Outline     │ ← 结构化大纲，分配各节字数和引用
│  (论文大纲生成)     │
└──────────┬───────┘
           ▼
┌──────────────────┐
│  Paper Writing     │ ← 逐节写作，保持连贯性和引用完整性
│  (论文写作)        │
└──────────┬───────┘
           ▼
┌──────────────────┐
│   Peer Review      │ ← 真实学者人设评审 + 评分 + 修改建议
│  (模拟同行评审)     │    → 自动修订 → 最终论文
└──────────┬───────┘
           ▼
[完整论文输出 (Markdown / LaTeX)]
```

### 2.2 目录结构

```
literature-paper-breaker/
├── src/
│   ├── data_sources/           # 学术数据库连接器
│   │   ├── base.py             # DataSource ABC, Paper 数据模型, Discipline 枚举
│   │   ├── openalex.py         # OpenAlex (免费, 240M+ 作品)
│   │   ├── semantic_scholar.py # Semantic Scholar (AI 驱动搜索)
│   │   ├── crossref.py         # CrossRef (DOI 元数据)
│   │   ├── core_ac.py          # CORE (开放获取全文)
│   │   ├── ctext.py            # 中国哲学书电子化计划 (古典文献)
│   │   └── aggregator.py       # 多源聚合搜索 + 去重 + 排序
│   ├── pipeline/               # 研究流水线
│   │   ├── orchestrator.py     # 总控协调器 (ResearchConfig, ResearchOrchestrator)
│   │   ├── literature_review.py # 系统性综述生成
│   │   ├── gap_analyzer.py     # 研究空白识别
│   │   ├── hypothesis_generator.py # 研究问题/假说生成
│   │   └── peer_review.py      # 同行评审模拟 (学者发现+评审+综合+修订)
│   ├── paper_engine/           # 论文写作引擎
│   │   ├── outliner.py         # 结构化大纲生成
│   │   └── writer.py           # 逐节论文写作
│   ├── utils/
│   │   └── llm.py              # LLM 提供商抽象层 (Anthropic/OpenAI/OpenRouter)
│   └── cli.py                  # CLI 命令行接口
├── scripts/
│   ├── dry_run.py              # 干跑模拟 (Mock LLM + Mock API, 验证全流程逻辑)
│   ├── run_papers.py           # 生产运行器 (真实API调用, 批量生成论文)
│   └── generate_images.py      # 🆕 图片生成 (Gemini 3.1 Flash via OpenRouter)
├── config/
│   └── default.yaml            # 默认配置文件
├── visualization/
│   ├── serve.py                # 可视化仪表板服务器
│   └── index.html              # 可视化前端
├── examples/
│   ├── example_economics.py    # 经济学示例
│   └── example_history.py      # 历史学示例
├── tests/
│   ├── test_data_sources.py    # 数据源测试
│   └── test_pipeline.py        # Pipeline 测试
├── output/                     # 生成的论文输出目录
├── pyproject.toml              # 项目配置 (依赖、构建、工具)
├── PROMOTION_PLAN.md           # 推广宣传计划
└── README.md                   # 项目 README
```

---

## 3. 核心模块详解

### 3.1 数据源层 (`src/data_sources/`)

#### `base.py` — 基础抽象

- `Paper`: Pydantic 数据模型，包含 title, authors, abstract, year, doi, journal, citations_count, keywords, source, full_text 等字段
- `Discipline`: 枚举类，包含 14 个学科方向
- `SearchResult`: 搜索结果封装，含分页信息
- `DataSource`: 抽象基类，定义 `search()` 和 `close()` 接口

#### `aggregator.py` — 多源聚合

- `AggregatedSource`: 并行调用所有启用的数据源，基于 DOI 去重，按引用量和相关性排序
- 支持动态添加/移除数据源

#### 各数据源

| 数据源 | 文件 | 特点 |
|--------|------|------|
| OpenAlex | `openalex.py` | 免费，240M+ 作品，推荐首选 |
| Semantic Scholar | `semantic_scholar.py` | AI 驱动搜索，引用图谱强 |
| CrossRef | `crossref.py` | DOI 元数据解析 |
| CORE | `core_ac.py` | 开放获取全文，需 API key |
| CText | `ctext.py` | 中国古典文献，十三经、二十四史等 |

### 3.2 研究流水线 (`src/pipeline/`)

#### `orchestrator.py` — 总控协调器

- `ResearchConfig`: 完整配置数据类，包括 topic, discipline, language, depth, llm_provider, llm_model, enabled_sources, enable_peer_review 等
- `ResearchSession`: 会话状态追踪，记录每个阶段的输出和错误
- `ResearchOrchestrator`: 核心协调器
  - `run_full_pipeline()`: 运行全部 6 个阶段（含可选同行评审）
  - `run_review_only()`: 仅运行文献综述
  - `_save_outputs()`: 将所有结果保存为 Markdown/LaTeX + JSON

#### `literature_review.py` — 文献综述

- 搜索学术数据库 → 收集论文 → LLM 分析 → 生成结构化综述
- 输出：主题分类、研究趋势、方法论脉络、关键争议、时间线叙事

#### `gap_analyzer.py` — 研究空白分析

- 输入：论文集 + 主题 + 已识别主题
- 输出：理论盲区、方法论局限、矛盾发现、未探索领域
- 每个 gap 标注 severity, addressable, gap_type

#### `hypothesis_generator.py` — 假说/问题生成

- 根据 discipline_type 生成：
  - **humanities**: 解释性研究问题
  - **social_science**: 可检验假说
- 输出：问题、假说、理论框架、方法论建议、预期贡献、可行性/新颖性评分
- 自动推荐最佳提案

#### `peer_review.py` — 同行评审模拟

- `PeerReviewer`: 核心评审器
  1. **学者发现** — 用 LLM + Semantic Scholar API 查找该领域真实学者
  2. **个体评审** — 以真实学者人设撰写评审意见（7 项评分标准，每项 1-10 分）
  3. **综合评审** — 汇总所有评审意见，给出共识决定和修订指令
  4. **自动修订** — 根据评审意见修改论文

### 3.3 论文写作引擎 (`src/paper_engine/`)

#### `outliner.py` — 大纲生成

- 根据选定的研究提案生成结构化大纲
- 包含：标题、摘要草稿、各节（标题、描述、要点、预估字数、所需引用、子节）
- 支持嵌套子节

#### `writer.py` — 论文写作

- `PaperWriter.write()`: 逐节写作
  1. 先写摘要
  2. 按大纲顺序逐节撰写（含子节递归）
  3. 每节输入前文上下文 + 可用引用 + 该节要求
- `PaperDraft`: 论文草稿数据类
  - `to_markdown()`: 导出为 Markdown
  - `to_latex()`: 导出为 LaTeX

### 3.4 LLM 抽象层 (`src/utils/llm.py`)

```python
LLMConfig(
    provider="openrouter",           # anthropic | openai | openrouter
    model="deepseek/deepseek-chat",  # 模型 ID
    api_key="",                      # 自动从环境变量读取
    base_url="",                     # openrouter 自动设为 https://openrouter.ai/api/v1
    max_tokens=8192,
    temperature=0.3,
)
```

- `LLMClient.generate()`: 文本生成（支持 system prompt）
- `LLMClient.generate_structured()`: 结构化 JSON 输出
- `UsageTracker`: Token 使用量和成本追踪

---

## 4. LLM 多模型策略

### 4.1 模型选择矩阵

| 用途 | 推荐模型 | Provider | 价格 (input/output per 1M tokens) | 说明 |
|------|---------|----------|-----------------------------------|------|
| **主力写作** | `deepseek/deepseek-chat` | OpenRouter | $0.24 / $0.38 | V3.2，90%+ 前沿质量，极致性价比 |
| **高质量任务** | `anthropic/claude-sonnet-4` | Anthropic | $3.00 / $15.00 | 最佳质量，贵 |
| **图片生成** | `google/gemini-3.1-flash-image-preview` | OpenRouter | $0.50 / $3.00 (文本) + $60/M (图片) | Nano Banana 2，Pro 级视觉质量 |
| **简单任务** | `google/gemini-3.1-flash-lite-preview` | OpenRouter | 极低 | 分类、摘要、简单提取等 |
| **备选经济** | `qwen/qwen-2.5-72b-instruct` | OpenRouter | $0.04 / $0.10 | 最便宜的高质量模型 |

### 4.2 分层调用策略

```
┌─────────────────────────────────────────────────┐
│  Tier 1: 核心写作 (deepseek/deepseek-chat)       │
│  ├── 文献综述生成                                 │
│  ├── 论文各节写作                                 │
│  ├── 同行评审意见                                 │
│  └── 论文修订                                    │
├─────────────────────────────────────────────────┤
│  Tier 2: 简单任务 (gemini-3.1-flash-lite)        │
│  ├── 搜索结果排序和过滤                            │
│  ├── 文本分类（学科、语言）                         │
│  ├── 简单摘要提取                                 │
│  ├── 引用格式化                                   │
│  └── 数据清洗和标准化                              │
├─────────────────────────────────────────────────┤
│  Tier 3: 图片生成 (gemini-3.1-flash-image)       │
│  ├── Pipeline 架构图                             │
│  ├── 论文样本截图                                 │
│  ├── 数据诚信对比图                               │
│  ├── 信息图（infographic）                        │
│  └── 社交媒体素材                                 │
└─────────────────────────────────────────────────┘
```

### 4.3 环境变量

```bash
# 主力模型 (OpenRouter)
export OPENROUTER_API_KEY="sk-or-v1-..."

# 高质量备选
export ANTHROPIC_API_KEY="sk-ant-..."
export OPENAI_API_KEY="sk-..."

# 数据源
export CORE_API_KEY="..."  # 可选，用于 CORE 全文检索
```

---

## 5. 图片生成能力（Gemini 3.1 Flash）

### 5.1 概述

通过 OpenRouter API 调用 `google/gemini-3.1-flash-image-preview`（代号 Nano Banana 2），可以为项目生成：
- Pipeline 架构流程图
- 论文样本截图风格图
- 数据诚信对比信息图
- 社交媒体推广素材

### 5.2 API 调用方式

使用 OpenAI 兼容接口，通过 OpenRouter 网关：

```python
from openai import AsyncOpenAI

client = AsyncOpenAI(
    api_key="sk-or-v1-...",
    base_url="https://openrouter.ai/api/v1",
)

response = await client.chat.completions.create(
    model="google/gemini-3.1-flash-image-preview",
    messages=[
        {"role": "user", "content": "Generate a clean infographic showing..."}
    ],
    # 关键参数：启用图片输出
    extra_body={
        "modalities": ["image", "text"],
    },
)

# 响应中的图片以 base64 data URL 返回
# 在 message.content 中查找 data:image/png;base64,... 格式的内容
```

### 5.3 图片生成 Prompt 技巧

来源于 Google Developers Blog 和社区最佳实践：

**核心原则：描述场景，不要列关键词。**

```
# 好的 prompt
"A clean, modern infographic showing a research pipeline with 7 steps flowing
from left to right. Each step is a rounded rectangle with an icon: Literature
Search (magnifying glass), Literature Review (book), Gap Analysis (puzzle piece),
Hypothesis Generation (lightbulb), Paper Outline (list), Paper Writing (pen),
Peer Review (checkmark). Steps are connected by arrows. Use a blue-to-purple
gradient color scheme on white background. Professional, minimalist academic style."

# 不好的 prompt
"pipeline, 7 steps, research, academic, infographic"
```

**摄影/电影语言控制构图**：
- "wide-angle shot" — 全景
- "macro shot" — 微距
- "85mm portrait lens" — 人像镜头
- "low-angle perspective" — 低角度

**信息图专用技巧**：
- 明确指定 **主题**、**受众**、**标题位置**、**数据/内容**
- Gemini 3.1 Flash 可从真实知识库提取信息生成更准确的内容
- 支持多语言 prompt，中文效果也不错

### 5.4 Gemini Flash Lite 用途

`google/gemini-3.1-flash-lite-preview` 作为更便宜的小模型，适合不需要深度思考的任务：

```python
# 用 Flash Lite 做简单分类
response = await client.chat.completions.create(
    model="google/gemini-3.1-flash-lite-preview",
    messages=[
        {"role": "system", "content": "Classify the following paper into one discipline."},
        {"role": "user", "content": paper_abstract}
    ],
    max_tokens=50,
    temperature=0.1,
)
```

适用场景：
- 论文学科分类
- 关键词提取
- 语言检测
- 简单摘要（< 100 字）
- 引用格式转换
- 布尔判断（是否相关、是否重复等）

---

## 6. 安装与配置

### 6.1 安装

```bash
# 基础安装
pip install -e ".[llm]"

# 完整安装（含开发工具）
pip install -e ".[full]"
```

**依赖**：Python >= 3.10，核心依赖包括 httpx, pydantic, rich, click, jinja2, pyyaml, tiktoken, tenacity, aiofiles, python-dotenv。LLM 可选依赖为 anthropic 和 openai。

### 6.2 配置文件

复制 `config/default.yaml` 为 `config/local.yaml` 进行自定义：

```yaml
research:
  depth: deep              # quick | standard | deep
  max_papers: 60
  language: zh
  discipline_type: humanities

llm:
  provider: openrouter
  model: deepseek/deepseek-chat
  temperature: 0.3
  max_tokens: 8192

sources:
  - openalex
  - semantic_scholar
  - crossref
  - ctext                 # 启用中国古典文献

peer_review:
  enabled: true
  num_reviewers: 3
  review_rounds: 1

paper:
  type: research_article
  target_words: 8000
  format: markdown
  citation_style: apa

output_dir: output
```

### 6.3 环境变量

```bash
# .env 文件
OPENROUTER_API_KEY=sk-or-v1-...
ANTHROPIC_API_KEY=sk-ant-...       # 可选
OPENAI_API_KEY=sk-...              # 可选
CORE_API_KEY=...                   # 可选，用于 CORE 全文
```

---

## 7. 使用指南

### 7.1 CLI 命令

```bash
# 完整研究流水线
lpb research "数字孪生与非物质文化遗产保护" \
  --discipline anthropology \
  --language zh \
  --depth deep \
  --target-words 10000 \
  --provider openrouter \
  --model deepseek/deepseek-chat

# 仅文献综述
lpb review "Confucian ethics in modern corporate governance" \
  --discipline philosophy

# 学术数据库搜索
lpb search "digital humanities methodology" -n 20

# 查看可用数据源
lpb sources
```

**完整 CLI 选项**：

| 选项 | 说明 | 默认值 |
|------|------|--------|
| `-d, --discipline` | 学科 | general |
| `-l, --language` | 语言代码 (en, zh, fr...) | en |
| `-yf, --year-from` | 起始年份 | 无 |
| `-yt, --year-to` | 结束年份 | 无 |
| `-n, --max-papers` | 最大论文数 | 50 |
| `--depth` | 综述深度 (quick/standard/deep) | standard |
| `--paper-type` | research_article/review/essay/commentary | research_article |
| `--discipline-type` | humanities / social_science | social_science |
| `-w, --target-words` | 目标字数 | 8000 |
| `-o, --output-dir` | 输出目录 | output/ |
| `--format` | 输出格式 (markdown/latex) | markdown |
| `--provider` | LLM 提供商 | anthropic |
| `--model` | 模型名 | claude-sonnet-4 |
| `--sources` | 数据源（逗号分隔） | openalex,semantic_scholar,crossref |

### 7.2 编程接口

```python
import asyncio
from src.data_sources.base import Discipline
from src.pipeline.orchestrator import ResearchConfig, ResearchOrchestrator

async def main():
    config = ResearchConfig(
        topic="认知语言学中的隐喻理论演变",
        discipline=Discipline.LINGUISTICS,
        language="zh",
        depth="deep",
        max_papers=60,
        discipline_type="humanities",
        llm_provider="openrouter",
        llm_model="deepseek/deepseek-chat",
        enable_peer_review=True,
        num_reviewers=3,
    )

    orchestrator = ResearchOrchestrator(config)

    async def on_progress(stage, msg):
        print(f"[{stage}] {msg}")

    session = await orchestrator.run_full_pipeline(on_progress)

    print(f"Papers found: {len(session.review_result.papers)}")
    print(f"Gaps identified: {len(session.gap_result.gaps)}")
    print(f"Peer review score: {session.peer_review_result.average_score:.1f}/10")
    print(session.draft.to_markdown())

asyncio.run(main())
```

### 7.3 干跑模拟

在不消耗 API 额度的情况下验证全流程逻辑：

```bash
python scripts/dry_run.py
```

这会使用 Mock LLM 和 Mock API 跑完所有阶段，输出验证结果和成本估算。

### 7.4 批量生产运行

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
python scripts/run_papers.py
```

默认生成 3 篇论文（英文社会学 + 中文人类学 + 英文哲学），使用 DeepSeek V3.2，预算 $25，实际成本 < $1。

---

## 8. 数据源详解

| 数据源 | 覆盖量 | 认证 | 全文 | 引用 | 费用 | 最佳场景 |
|--------|--------|------|------|------|------|---------|
| **OpenAlex** | 240M+ 作品 | 无需 | 否 | 是 | 免费 | 通用首选，覆盖最广 |
| **Semantic Scholar** | 200M+ 论文 | 可选(提高限速) | 否 | 是 | 免费 | 引用关系分析、AI/CS领域 |
| **CrossRef** | DOI 元数据 | 无需 | 否 | 否 | 免费 | DOI 解析、出版信息 |
| **CORE** | 开放获取 | API key | 是 | 否 | 免费 | 需要全文时 |
| **CText** | 中国古典 | 无需 | 是 | 否 | 免费 | 先秦两汉经典、哲学研究 |

**聚合搜索流程**：
1. 并行查询所有启用的数据源
2. 基于 DOI 去重
3. 按引用量 + 相关性加权排序
4. 返回统一的 `SearchResult`

---

## 9. 输出格式与文件结构

一次完整运行后，`output/` 目录包含：

```
output/
├── literature_review.md    # 系统性文献综述（含主题分析、趋势、论文列表）
├── gap_analysis.md         # 研究空白（每个 gap 含类型、严重性、可行性）
├── proposals.md            # 研究提案（含推荐标记、方法论、理论框架）
├── paper.md                # 完整论文草稿（或 paper.tex）
├── references.json         # 结构化引用数据
├── timeline.json           # 研究发展时间线
└── peer_review.md          # 同行评审报告（含个体评审、综合评审、修订指令）
```

---

## 10. 开发指南

### 10.1 开发环境

```bash
pip install -e ".[dev]"
pytest                # 运行测试
ruff check src/       # 代码检查
mypy src/             # 类型检查
```

### 10.2 添加新数据源

1. 在 `src/data_sources/` 创建新文件
2. 继承 `DataSource` 抽象基类
3. 实现 `search()` 和 `close()` 方法
4. 在 `orchestrator.py` 的 `_init_sources()` 中注册

### 10.3 技术栈

- **Python 3.10+**
- **异步架构**: asyncio + httpx (异步 HTTP)
- **数据模型**: Pydantic v2
- **CLI**: Click
- **模板**: Jinja2
- **Token 计数**: tiktoken
- **重试**: tenacity
- **终端美化**: Rich

---

## 11. 成本估算

基于干跑模拟的 LLM 调用模式估算：

| 模型 | 每篇论文成本 | 3 篇论文 |
|------|------------|---------|
| `deepseek/deepseek-chat` (V3.2) | ~$0.05 | ~$0.15 |
| `google/gemini-2.0-flash-001` | ~$0.03 | ~$0.09 |
| `anthropic/claude-sonnet-4` | ~$0.50 | ~$1.50 |

**图片生成成本** (Gemini 3.1 Flash Image)：
- 0.5K 分辨率：~$0.045/张
- 4K 分辨率：~$0.15/张
- 生成 10 张推广素材：~$0.50-1.50

---

## 12. 推广计划摘要

详见 [`PROMOTION_PLAN.md`](./PROMOTION_PLAN.md)。

### 核心策略

1. **Phase 1 (1-2周)**: 基础建设 — README 改造、Pipeline 架构图、Demo GIF、示例论文
2. **Phase 2 (3-4周)**: 首发推广 — Twitter Thread、Hacker News、知乎深度文章、B站视频
3. **Phase 3 (5周+)**: 持续运营 — 每周内容输出、社区建设、用户showcase

### 核心宣传话术

> **其他AI论文工具会编造调研数据，我们不会。**
>
> Literature Paper Breaker 是首个专为人文社科设计的AI论文研究引擎。它搜索真实学术数据库、生成真正的文献综述，而且——关键的是——永远不会伪造实证数据。当你的研究需要人类受试者时，它会写一份规范的研究方案，而不是编造假统计数字。
>
> 一行命令，从选题到论文。

### 推广素材生成

使用 `scripts/generate_images.py` 自动生成推广所需的视觉素材：

```bash
export OPENROUTER_API_KEY="sk-or-v1-..."
python scripts/generate_images.py
```

生成内容包括 Pipeline 架构图、数据诚信对比图、论文样本展示图、社交媒体素材等。

---

*文档最后更新: 2026-03-10*
