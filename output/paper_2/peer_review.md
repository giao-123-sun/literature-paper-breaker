# 同行评审报告（第一轮）

**论文标题**：数字孪生与非物质文化遗产保护：人工智能时代传统手工艺知识图谱的构建与传承路径研究

**投稿期刊**：《文化遗产》（假拟）

**平均得分**：6.8/10

**综合决定**：major_revision（大修）

---

## 编辑综合意见

### 综述

三位评审人一致认为本文选题具有重要的学术价值和实践意义，将数字孪生、知识图谱与非物质文化遗产传承三个领域进行交叉整合的思路具有创新性。然而，评审人也共同指出了若干需要重点修改的问题。

### 关键优点

- 研究选题前沿且具有跨学科整合的理论雄心，填补了非遗数字孪生领域的理论空白
- 提出的"五层数字孪生架构"和TCKO本体具有一定的原创性和理论贡献
- 伦理反思部分的讨论较为深入，体现了人文关怀

### 核心问题

1. **实证基础薄弱**：全文停留在理论构想层面，缺乏原型系统的实现或哪怕最小规模的实验验证，这严重削弱了论文的说服力
2. **TCKO本体设计缺乏形式化规范**：本体仅以自然语言描述，缺少OWL/RDF形式化定义、competency questions的验证以及与CIDOC-CRM具体映射关系的技术细节
3. **案例讨论流于表面**：苏绣与景德镇陶瓷的案例仅为概念性描述，未提供任何数据采集、知识建模或系统实现的细节
4. **文献综述覆盖面不足**：缺少对具身认知理论（embodied cognition）、实践知识哲学（如Polanyi隐性知识理论）等重要理论基础的系统引用

### 修改指导

请作者针对以下方面进行重点修改：（1）补充至少一个案例的初步实证数据或原型系统验证，即使是小规模概念验证（proof-of-concept）也可以；（2）对TCKO本体提供形式化定义，包括OWL类层次结构图、核心属性的domain/range定义、以及与CIDOC-CRM标准类的具体映射表；（3）深化文献综述，特别是具身认知理论和隐性知识哲学的相关文献；（4）在方法论部分更清晰地界定本文的研究方法和论证逻辑；（5）回应各评审人提出的具体修改意见。

---

## 评审人评审意见

---

### 评审人1：党安荣

**所属机构**：清华大学建筑学院 | **研究方向**：数字孪生与文化遗产 | **h-index**: ~25

**综合评分**：7.0/10 | **录用决定**：minor_revision（小修）

#### 评分细则

| 评价维度 | 分数 | 评语 |
|---------|------|------|
| 原创性 | 7/10 | 将数字孪生从物质遗产领域扩展至非遗领域的思路有新意，"五层架构"有一定原创性，但"语义层"的概念与已有数字孪生信息模型（如ISO 23247）的关系未予澄清 |
| 理论框架 | 7/10 | 框架整体逻辑清晰，五个层次之间的递进关系合理，但各层之间的数据流转机制和接口标准描述不够具体 |
| 方法论 | 6/10 | 作为理论框架类论文可以理解，但全文缺少明确的研究方法论说明——是概念分析、设计科学研究还是系统性综述？需要交代清楚 |
| 文献综述 | 7/10 | 对数字孪生在文化遗产领域的文献把握较好，引用了Boscaro等的最新综述，但对数字孪生技术本身的发展脉络（如Grieves-Vickers的DT成熟度模型、NASA的DT路线图）介绍不足 |
| 论证与证据 | 6/10 | 论证逻辑基本通顺，但关键主张缺乏实证支撑。例如，"双向耦合"机制的可行性仅有概念性描述，未提供任何技术验证 |
| 写作质量 | 8/10 | 行文流畅，结构清晰，学术语言运用规范。部分术语的中英文对照处理得当 |
| 学术意义 | 7/10 | 选题具有重要的学术价值和应用前景，但当前论文的贡献主要在概念层面，距离可落地的学术贡献仍有距离 |

#### 优点

1. 将数字孪生的应用边界从物质文化遗产拓展至非物质文化遗产，提出了有意义的理论视角。这一扩展回应了当前数字孪生研究过于聚焦建筑与遗址的学科偏见
2. "五层数字孪生架构"的设计兼顾了技术可行性和非遗特殊性，特别是"感知层"对多模态数据采集的规划和"语义层"对知识图谱嵌入的设想有前瞻性
3. 文献综述部分对三条技术路径的梳理较为系统，对五个研究缺口的识别精准且有说服力
4. 伦理反思部分的"记录性原真性"与"实践性原真性"的区分有独到见解

#### 不足

1. 全文缺乏对数字孪生技术实现细节的讨论。五层架构中的"模型层"涉及几何模型、行为模型和过程模型，但对每类模型的建模方法、计算复杂度、数据需求等均未展开说明。作为建筑学和地理信息科学背景的研究者，我认为这些技术细节是不可或缺的
2. "感知层"列出了多种传感设备和数据采集方案，但对实际部署的可行性缺乏讨论。例如，在传承人的日常工作场景中部署惯性动捕和力传感设备是否会干扰其正常操作？数据采集的精度要求和成本约束如何？
3. 对"数字孪生"概念的使用过于宽泛。按照Grieves和Vickers的经典定义，数字孪生要求物理实体与虚拟模型之间的实时数据同步，而非遗手工艺的"过程"本质上是非重复的、创造性的，每次操作都不相同。论文需要更深入地讨论这一本体论张力
4. 两个案例（苏绣、景德镇陶瓷）的讨论过于概略，未能展示CIIS框架在具体场景中的操作化路径

#### 详细评审意见

本文试图在非遗保护领域引入数字孪生和知识图谱的整合框架，这一研究方向我高度认同。在我自己的研究实践中，数字孪生在长城等物质遗产保护中的应用已经取得了一些进展，但向非遗领域的扩展确实面临根本性的理论和技术挑战。作者识别的五个研究缺口准确反映了当前领域的现状，这表明作者对文献有较好的把握。

然而，我的主要关切在于论文的"技术着地性"不足。五层架构和TCKO本体作为概念性框架有其价值，但在缺乏任何实证验证的情况下，读者无法判断这些框架的技术可行性。特别是"双向耦合"机制——知识图谱驱动数字孪生的参数化模拟、模拟结果反馈更新知识图谱——这一核心技术路径需要至少一个概念验证实验来支撑。我建议作者选择苏绣中的一种基本针法（如齐针），展示从数据采集、知识建模到数字孪生模拟的完整流程，即使是简化版也好。

另外，文章对"数字孪生"概念的适用性缺乏批判性反思。工业数字孪生的核心在于预测性——通过虚拟模型预测物理实体的未来状态。但手工艺过程的核心恰恰在于不可预测性和创造性——优秀传承人的价值正在于其独特的艺术判断和即兴发挥。文章需要正面回应这一矛盾，而不是简单地将工业领域的概念平移到文化遗产领域。

#### 修改建议

1. 补充数字孪生成熟度模型的文献（如Grieves-Vickers模型或Kritzinger等的分类），明确CIIS系统在数字模型、数字影子、数字孪生三个层次中的定位
2. 为至少一个案例（建议选择苏绣齐针）提供初步的概念验证数据或原型系统截图
3. 在感知层的讨论中增加对数据采集可行性和成本的分析
4. 正面讨论数字孪生"可预测性"范式与手工艺"创造性"本质之间的张力，明确CIIS的技术定位（是预测型、描述型还是规范型数字孪生？）

---

### 评审人2：杨红

**所属机构**：中国传媒大学文化产业管理学院 | **研究方向**：非物质文化遗产数字化传播 | **h-index**: ~15

**综合评分**：6.5/10 | **录用决定**：major_revision（大修）

#### 评分细则

| 评价维度 | 分数 | 评语 |
|---------|------|------|
| 原创性 | 7/10 | 将数字孪生与知识图谱整合用于非遗传承的思路有新意。我在2023年的研究中曾将非遗数字化迁移类比为"数字孪生行为"，本文在此基础上进行了系统化建构，值得肯定 |
| 理论框架 | 6/10 | 框架的技术导向明显，但对非遗传承的文化维度、社会维度和教育维度关注不足。"五层架构"几乎完全从技术视角出发，缺少"人"的位置 |
| 方法论 | 6/10 | 研究方法不够清晰。文章同时包含文献综述、理论建构和案例讨论，但各部分之间的方法论衔接不流畅 |
| 文献综述 | 6/10 | 对技术类文献的综述较为充分，但对非遗研究领域的核心文献覆盖不足。缺少对非遗传承教育学、社区参与式保护、非遗生产性保护等重要议题的文献讨论 |
| 论证与证据 | 6/10 | 技术方案的描述停留在概念层面，缺乏操作化路径。案例讨论未能充分展示框架的应用价值 |
| 写作质量 | 7/10 | 整体写作质量较好，但部分技术术语的使用可能对非遗研究领域的读者构成阅读障碍 |
| 学术意义 | 7/10 | 研究选题重要，跨学科整合的尝试值得鼓励，但需要更好地平衡技术视角和人文视角 |

#### 优点

1. 研究选题回应了非遗保护领域的真实需求——传统手工艺隐性知识的数字化表征确实是当前面临的核心难题，本文提出的整合方案有针对性
2. 对"原真性"问题的伦理讨论有深度，"记录性原真性"与"实践性原真性"的区分有助于厘清数字化保护的边界与定位
3. 引用了我2023年的研究并有所发展，体现了作者对非遗数字化传播领域研究脉络的了解
4. 五个研究缺口的识别具有综合性和前瞻性

#### 不足

1. **传承人视角的缺失**：全文以技术研发者的视角展开，传承人在整个框架中被定位为"数据源"（感知层的数据采集对象）和"用户"（应用层的教学对象），而非主体性的参与者和决策者。这与文章伦理部分倡导的"传承人主体性"形成矛盾
2. **社区参与机制的空洞化**：缺口五提出"社区参与和伦理治理机制缺失"，但论文自身在这方面的建构同样薄弱。如何让传承人参与知识图谱的构建和验证？如何在技术开发过程中实现真正的"共同设计"（co-design）？这些关键问题缺乏具体方案
3. **非遗传承的教育维度被忽视**：传统手工艺的师徒传承不仅是"知识转移"，更是一种社会化过程，涉及价值观、职业伦理、审美判断等软性能力的养成。CIIS框架的"应用层"将传承简化为"交互式学习"，未能反映传承教育的复杂性
4. **文献综述的学科偏差**：综述以技术类文献为主，对非遗保护领域的人文社科研究（如巴莫曲布嫫对非遗保护理念的研究、刘魁立对非遗传承规律的探讨、马盛德对非遗分类保护的研究等）关注不足，导致理论框架的学科基础不够均衡

#### 详细评审意见

作为长期从事非遗数字化传播研究的学者，我认为本文的选题方向是正确的——数字孪生和知识图谱确实有可能为非遗保护提供新的技术手段。然而，本文最大的问题在于过度的"技术中心主义"倾向。

非遗保护的核心理念是"以人为本"——传承人是非遗的核心载体，社区是非遗的文化土壤。本文提出的CIIS框架虽然在伦理反思部分提到了传承人主体性，但整个技术框架的设计逻辑实际上是"以技术为中心"的：先设计技术架构，再考虑如何将人纳入其中。更理想的路径应该反过来——先深入理解传承人的真实需求和传承实践的内在逻辑，再设计技术方案来回应这些需求。

我建议作者在修改中进行以下根本性的视角调整：在五层架构中明确增加"社区参与层"或在每一层中嵌入传承人参与的机制。例如，在"语义层"的知识图谱构建中，不仅需要NLP技术的自动抽取，更需要传承人对知识节点和关系的确认、修正和补充——这是保证知识图谱"文化正确性"的关键。在"应用层"中，不仅要设计面向学徒的教学功能，还要设计面向传承人的知识管理和自我表达工具，让传承人不仅是被记录的对象，更是主动的知识生产者。

此外，我希望作者能更好地处理"技术可能性"与"实践必要性"之间的关系。文章描述了许多技术上可能实现的功能（如力反馈模拟、窑变预测等），但这些功能是否真正回应了传承人和非遗保护机构的实际需求？建议作者补充一些田野调查或访谈数据，了解传承人和保护工作者对数字化工具的真实态度和期望。

#### 修改建议

1. 在五层架构中增加"参与性设计"（participatory design）维度，在每个层次中明确传承人和社区的参与方式和决策权限
2. 补充非遗保护领域的人文社科核心文献，特别是关于传承教育、社区参与、生产性保护等议题的研究
3. 在案例讨论部分补充对传承人的初步访谈或田野观察数据，了解其对数字化工具的需求和态度
4. 在应用层中增加面向传承人的功能设计，使传承人不仅是"用户"更是"共同创作者"
5. 对技术方案的"必要性"进行论证——不仅要说明技术"能做什么"，还要论证"为什么需要这样做"

---

### 评审人3：Chiara Boscaro

**Institution**: Politecnico di Milano | **Research Focus**: Digital Twins for Cultural Heritage | **h-index**: ~10

**Overall Score**: 6.8/10 | **Decision**: major_revision

#### Scoring Criteria

| Criterion | Score | Comment |
|-----------|-------|---------|
| Originality | 7/10 | The extension of digital twin concepts from tangible to intangible cultural heritage is a meaningful contribution. The five-layer architecture and the notion of "semantic twinning" are interesting, though the novelty relative to existing DT reference architectures (e.g., ISO 23247, DTDL) needs clarification |
| Theoretical Framework | 7/10 | The framework is logically structured and addresses a real gap. However, the relationship between the proposed architecture and established DT maturity models is not discussed. In our 2025 survey, we emphasized that most heritage DT implementations remain at early maturity stages; this paper should position CIIS within such a maturity spectrum |
| Methodology | 5/10 | This is the paper's weakest dimension. There is no clear methodological statement. The paper oscillates between literature review, conceptual framework design, and speculative case discussion without a coherent research design. The absence of any empirical validation—even a small-scale proof-of-concept—significantly limits the contribution |
| Literature Review | 7/10 | The review covers relevant recent literature, including our own systematic review. However, several important works are missing: (1) the FAIR principles for heritage data; (2) recent work on Heritage BIM (HBIM) and its ontological foundations; (3) the ISO 21127 (CIDOC-CRM) implementation guidelines, which are critical if TCKO is to be positioned as a CRM extension |
| Argumentation & Evidence | 6/10 | The argumentation is generally logical but insufficiently supported. Key claims—especially regarding the bidirectional coupling mechanism—remain at the level of aspiration rather than demonstration. The case discussions do not provide enough detail to assess feasibility |
| Writing Quality | 7/10 | The paper is well-written in Chinese with clear structure. Technical terminology is generally used accurately. Some English terms could benefit from more precise usage (e.g., "digital twin" vs. "digital shadow" vs. "digital model") |
| Significance | 7/10 | The topic is timely and the interdisciplinary ambition is commendable. If the framework can be validated, it would represent a significant contribution to both digital heritage and ICH preservation fields |

#### Strengths

1. The identification of five research gaps is well-grounded in the literature and accurately captures the current state of the field. The gap regarding the absence of DT theoretical frameworks for ICH is particularly well-articulated
2. The TCKO ontology, while needing formalization, introduces relevant classes (especially `EmbodiedSkill` and `AestheticJudgment`) that address genuine limitations of existing heritage ontologies such as CIDOC-CRM
3. The ethical discussion on authenticity, IP rights, and AI innovation boundaries is thoughtful and adds important nuance to what could otherwise be a purely technical paper
4. The paper engages substantively with our 2025 survey findings, correctly identifying the maturity gap in heritage DT implementations

#### Weaknesses

1. **Lack of formalization for TCKO**: The ontology is described only in natural language. For a knowledge engineering contribution, this is insufficient. The paper should provide: (a) formal class hierarchy in OWL notation or equivalent; (b) competency questions that the ontology is designed to answer; (c) a concrete mapping table showing how TCKO classes relate to specific CIDOC-CRM entities (e.g., does `CraftProcess` extend `E7 Activity` or `E29 Design or Procedure`?); (d) at minimum one instantiation example with real data
2. **Absence of empirical validation**: As we noted in our 2025 survey, the heritage DT field already suffers from a proliferation of conceptual frameworks without implementation. This paper risks adding another untested framework to the literature. Even a minimal proof-of-concept—e.g., constructing a small knowledge graph for one specific craft technique and linking it to a simple 3D simulation—would substantially strengthen the paper
3. **Imprecise use of DT terminology**: The paper does not distinguish between digital model (no automatic data flow), digital shadow (one-way data flow from physical to virtual), and digital twin (bidirectional data flow). According to Kritzinger et al.'s (2018) classification, what the paper describes appears to be closer to a "digital shadow" or at most a "digital model" rather than a true "digital twin." This distinction matters because it determines the technical requirements and feasibility
4. **Missing discussion of data standards and interoperability**: The paper proposes TCKO as a CIDOC-CRM extension but does not discuss how it would interface with existing heritage data standards (LIDO, Dublin Core, EDM) or linked data practices. Interoperability is crucial for knowledge graphs that aim to serve multiple stakeholders

#### Detailed Review Comments

This paper addresses an important gap in the digital heritage literature—the application of digital twin concepts to intangible cultural heritage, particularly traditional crafts. The interdisciplinary scope is ambitious, spanning digital twin engineering, knowledge graph construction, embodied cognition, and heritage ethics. I appreciate the authors' effort to bring these domains together.

However, my primary concern is methodological. The paper presents a theoretical framework without any form of validation, which makes it difficult to evaluate whether the proposed solutions are technically feasible or practically useful. In the digital twin community, there is growing awareness that the gap between conceptual architectures and working implementations is a major obstacle to progress. This paper, unfortunately, remains firmly on the conceptual side of that gap. The bidirectional coupling mechanism between knowledge graphs and digital twins—which the authors identify as the core innovation—is described only at a high level. How would semantic queries from the knowledge graph be translated into simulation parameters in real-time? What physics engines or simulation platforms are envisioned for modeling craft processes? How would the feedback loop from simulation to knowledge graph updates be implemented and validated? These questions need to be addressed, at least at a conceptual-technical level.

My second concern relates to the ontology contribution. TCKO introduces four new classes, which are conceptually relevant. However, ontology engineering follows established methodologies (e.g., Methontology, NeOn) that require competency questions, formalization, evaluation against use cases, and iterative refinement with domain experts. The paper does not follow any of these practices. Furthermore, the claim that TCKO extends CIDOC-CRM is made without sufficient technical detail—the mapping relationships are asserted but not demonstrated. I strongly recommend that the authors provide at least a partial formalization and one worked example showing how a specific craft technique (e.g., one Su embroidery stitch type) would be represented using TCKO.

#### Suggestions for Revision

1. Provide a formal specification of TCKO (at minimum in a semi-formal notation), including class hierarchy, object/data properties with domain and range, and explicit mappings to CIDOC-CRM entities. Include competency questions the ontology is designed to answer
2. Implement a minimal proof-of-concept: construct a small knowledge graph for one specific craft technique using TCKO, and demonstrate its connection (even if conceptual) to a digital representation of the craft process
3. Adopt Kritzinger et al.'s (2018) classification to precisely position CIIS within the digital model/shadow/twin spectrum, and discuss the technical implications of each level for ICH applications
4. Add a discussion of data interoperability standards (LIDO, Dublin Core, EDM) and linked data practices relevant to heritage knowledge graphs
5. Include a research methodology section that clearly states the research approach (e.g., design science research methodology per Hevner et al. 2004) and evaluation criteria

---

*评审日期：2026年3月*
*编辑：《文化遗产》编辑部*
