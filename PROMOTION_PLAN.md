# Literature Paper Breaker — 推广宣传计划

## 一、竞品分析总览

### 1.1 开源竞品（GitHub）

| 项目 | Stars | 定位 | 关键成功因素 |
|------|-------|------|-------------|
| **gpt_academic** | 68K+ | 中科院·学术GPT优化 | 中文生态、B站/知乎教程爆发、一键安装包 |
| **GPT-Researcher** | 25.6K | 自主深度研究Agent | Tavily创始人项目、Twitter推广、HN热帖 |
| **Sakana AI-Scientist** | 12.1K+2K(v2) | 全自动科学发现 | 学术论文+博客+媒体轰炸、$15/篇的震撼定价 |
| **Stanford STORM** | 18K+ | Wiki式报告生成 | 斯坦福品牌、在线Demo（7万人试用）|
| **AutoSurvey** | 460 | 自动综述写作 | NeurIPS 2024 主会论文 |

### 1.2 商业竞品

| 产品 | 用户量 | 定价 | 主要卖点 |
|------|--------|------|---------|
| **SciSpace** | 280M篇论文库 | $12/月 | AI读论文+写作+引用，Product Hunt 168票 |
| **Jenni AI** | 500万+学术用户 | $12-30/月 | AI自动补全、2600+引用格式、30+语言 |
| **笔灵AI** | 国内头部 | 按篇收费 | 700+学科、查重率15%、阿里云技术 |
| **万能小in** | 大量C端用户 | 免费/付费 | 3分钟5万字、130+场景 |
| **66AI论文** | - | 按篇收费 | 720学科、10秒千字大纲、查重率10% |

### 1.3 竞品推广策略模式分析

**模式A：学术可信度路线（AI-Scientist, AutoSurvey）**
- 先发顶会论文 → 博客发布 → 开源代码 → 媒体跟进
- 效果：高端用户信任，但受众窄

**模式B：开发者社区路线（gpt_academic, GPT-Researcher）**
- GitHub优质README → 社区教程 → B站/YouTube视频 → 知乎/HN讨论
- 效果：Stars快速增长，社区自发传播

**模式C：产品演示路线（Stanford STORM, SciSpace）**
- 在线Demo体验 → Product Hunt发布 → 用户口碑传播
- 效果：直接转化用户，7万人试用STORM

**模式D：C端流量路线（笔灵, 万能小in, 66AI）**
- 小红书图文种草 → 知乎SEO软文 → B站评测视频 → 百度SEM
- 效果：大量C端用户，但品牌溢价低

---

## 二、我们的差异化定位

### 核心差异点
Literature Paper Breaker 与所有竞品的本质区别：

1. **人文社科专精** — 竞品全部面向理工科/通用领域，无一专注人文社科
2. **全流程自动化** — 从文献检索→综述→研究空白→假说→大纲→全文→同行评审，端到端
3. **多学术数据库整合** — OpenAlex + Semantic Scholar + CrossRef + CORE + CText（中国古典文献）
4. **数据诚信保护** — 我们的系统会明确区分"可计算完成"vs"需要人工调研"，不编造数据
5. **中英文双语** — 可用中文写中文论文，竞品多为英文优先

### 推荐定位语

**英文**: "The first AI research pipeline built specifically for humanities & social sciences — from literature to publication-ready manuscript"

**中文**: "首个人文社科AI论文研究引擎 — 从文献检索到完整论文，全流程自动化"

---

## 三、推广计划

### Phase 1: 基础建设（第1-2周）

#### 3.1 GitHub README 改造
参考 gpt_academic 和 GPT-Researcher 的成功模式：

**必备元素：**
- [ ] **架构流程图** — 展示完整pipeline（文献检索→综述→空白分析→假说→大纲→写作→评审）
  - 工具：用 Mermaid 或 draw.io 制作
  - 参考：Sakana AI-Scientist 的4步流程图
- [ ] **Demo GIF/动画** — 录制一次完整的论文生成过程（加速版，30秒内）
  - 工具：asciinema（终端录制）或 screen recording
- [ ] **示例论文展示** — 精选1-2篇生成的论文，放在 `examples/` 目录
  - 标注哪些是计算分析（已完成），哪些是研究协议（待人工执行）
- [ ] **一键安装脚本** — gpt_academic 68K stars的关键因素之一
- [ ] **中英文双语README** — 覆盖两个市场
- [ ] **Badges** — Python版本、License、Stars计数

#### 3.2 Demo / 在线体验
Stanford STORM 的7万用户试用证明了在线Demo的威力：

- [ ] **Hugging Face Space** — 部署简化版在线体验
  - 输入主题 → 自动生成文献综述 + 研究提案
  - 不需要完整pipeline，只做前3步就足够震撼
- [ ] 或者搭建简单的 **Streamlit/Gradio Web UI**

#### 3.3 视觉素材准备

| 素材类型 | 用途 | 规格 |
|---------|------|------|
| **Pipeline架构图** | README、博客、推文 | 1200x600 PNG |
| **论文生成对比图** | 展示输入→输出 | 左右对比，1200x800 |
| **Before/After** | 体现AI辅助的价值 | 2-3张系列图 |
| **终端录屏GIF** | README嵌入 | 800x500, <5MB |
| **数据诚信特性图** | 差异化卖点展示 | 信息图，标注真/假数据区分 |
| **论文样本PDF截图** | 社交媒体素材 | 带标注的论文页面截图 |

### Phase 2: 首发推广（第3-4周）

#### 3.4 英文市场

**Twitter/X 发布（最重要）：**
- 发布一条Thread（3-5条推文的链式帖）
- 结构参考Sakana AI-Scientist的发布：
  1. Hook: "We built the first AI research pipeline designed specifically for humanities & social sciences 🧵"
  2. 问题陈述: "Existing AI paper tools are built for STEM. They hallucinate survey data and fabricate statistics..."
  3. 解决方案: Pipeline流程图 + 关键特性
  4. 示例展示: 生成的论文截图（标注数据诚信保护）
  5. CTA: GitHub链接 + 在线Demo链接

**发布时间**: 周二-周四 9-11 AM EST（数据显示B2B内容最佳时段）

**Hacker News 发布：**
- 标题格式: "Show HN: AI Research Pipeline for Humanities & Social Sciences"
- 准备好在评论区回答技术问题

**Reddit:**
- r/MachineLearning（Show ML帖）
- r/AcademicPhilosophy, r/AskSocialScience
- r/LanguageTechnology

#### 3.5 中文市场

**知乎（最重要）：**
- 发2-3篇深度文章：
  1. "我做了一个专门给人文社科用的AI论文引擎" — 技术故事 + 动机
  2. "AI写论文的致命缺陷：伪造调研数据" — 以数据诚信为切入点
  3. "用AI从0到1生成一篇人文社科论文是什么体验" — 实操教程

**B站：**
- 录制 10-15分钟演示视频
- 展示从输入主题到生成完整论文的过程
- 重点展示：文献检索结果、研究空白分析、论文输出、同行评审

**小红书：**
- 图文笔记：3-5张精选截图 + 简要说明
- 标签：#AI论文 #学术工具 #人文社科 #毕业论文
- 风格：清爽、学术感、突出"免费开源"

**微信公众号/技术社区：**
- CSDN 技术博客
- 掘金 技术文章
- 即刻 动态发布

### Phase 3: 持续运营（第5周+）

#### 3.6 内容持续输出

**每周内容节奏：**
- 周一：技术博客/知乎文章（深度内容）
- 周三：Twitter/X 更新（特性展示、用户反馈）
- 周五：B站/小红书（可视化内容）

**话题方向：**
- 用LPB分析某个热点人文话题（如"AI对集体记忆的影响"）
- 与其他工具的对比测评
- 用户生成的论文showcase
- 功能更新changelog

#### 3.7 社区建设
- GitHub Discussions 开启
- 创建 Discord 或微信群
- 定期回应 Issues
- 邀请人文社科学者试用并给反馈

---

## 四、需要准备的具体素材清单

### 4.1 必须有的图片素材

1. **Pipeline 架构图**
   ```
   [Topic Input] → [Literature Search] → [Literature Review] → [Gap Analysis]
        → [Hypothesis Generation] → [Paper Outline] → [Paper Writing] → [Peer Review]
        → [Revision] → [Final Paper]
   ```
   建议用彩色方块+箭头，每步标注使用的数据源和LLM

2. **论文样本截图**（3-4张）
   - 生成的论文首页（标题+摘要）
   - 方法论部分（展示研究协议vs已完成研究的区分）
   - 参考文献列表（展示真实引用）
   - 同行评审反馈页面

3. **数据诚信对比图**
   - 左边：其他AI工具"73%的受访者表示..."（伪造数据，标红）
   - 右边：LPB "本研究拟对60名大学生进行访谈..."（诚实的研究协议，标绿）

4. **支持的数据源 Logo 矩阵**
   - OpenAlex, Semantic Scholar, CrossRef, CORE, CText logos

### 4.2 可选的视频素材

1. **30秒快速Demo**（Twitter/X用）
   - 输入主题 → 论文生成 → 终端输出动画

2. **10-15分钟完整教程**（B站/YouTube）
   - 安装 → 配置 → 运行 → 结果解读

3. **2-3分钟概念介绍**（Product Hunt / 知乎用）
   - 问题 → 解决方案 → 展示 → CTA

### 4.3 论文展示样本

从现有 `output/` 选取最佳样本：
- Paper 1（英文）: "LLMs as Cultural Agents" — 展示跨语言分析能力
- Paper 2（中文）: "数字孪生与非物质文化遗产" — 展示中文能力
- 建议生成1-2篇新的短论文作为快速Demo案例

---

## 五、推广效果预期与KPI

### 第一个月目标
| 指标 | 目标值 | 对标 |
|------|--------|------|
| GitHub Stars | 500+ | AutoSurvey (460) 作为baseline |
| Twitter首发Thread | 50+ 转发, 200+ 赞 | — |
| 知乎文章 | 1000+ 赞同 | gpt_academic 知乎爆文 |
| B站视频 | 5000+ 播放 | — |
| HN帖子 | 前页上榜 | GPT-Researcher 的首发效果 |

### 三个月目标
| 指标 | 目标值 |
|------|--------|
| GitHub Stars | 3000+ |
| 在线Demo用户 | 5000+ |
| Discord/微信群 | 200+ 成员 |

---

## 六、关键行动优先级

| 优先级 | 行动项 | 预计工时 |
|--------|--------|---------|
| P0 | 制作Pipeline架构图 | 2h |
| P0 | 改造GitHub README（中英文） | 4h |
| P0 | 准备2-3篇示例论文截图 | 1h |
| P0 | 编写Twitter发布Thread | 1h |
| P1 | 录制终端Demo GIF | 2h |
| P1 | 部署Hugging Face Space / Web UI | 8h |
| P1 | 撰写知乎首发文章 | 3h |
| P1 | 制作数据诚信对比图 | 2h |
| P2 | 录制B站完整教程视频 | 4h |
| P2 | 小红书图文准备 | 1h |
| P2 | HN/Reddit帖子准备 | 1h |
| P2 | Product Hunt页面准备 | 3h |

---

## 七、核心宣传话术

### 英文版
> **Tired of AI paper tools that hallucinate survey data?**
>
> Literature Paper Breaker is the first AI research pipeline built specifically for humanities & social sciences. It searches real academic databases, generates genuine literature reviews, and — crucially — never fabricates empirical data. When your research needs human subjects, it writes a proper research protocol instead of inventing fake statistics.
>
> From topic to manuscript in one command.

### 中文版
> **其他AI论文工具会编造调研数据，我们不会。**
>
> Literature Paper Breaker 是首个专为人文社科设计的AI论文研究引擎。它搜索真实学术数据库、生成真正的文献综述，而且——关键的是——永远不会伪造实证数据。当你的研究需要人类受试者时，它会写一份规范的研究方案，而不是编造假统计数字。
>
> 一行命令，从选题到论文。
