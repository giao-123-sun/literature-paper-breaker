# Large Language Models as Cultural Agents: How AI-Generated Text Reshapes Collective Memory and Historical Narratives in the Digital Public Sphere

## *Revised Manuscript — Addressing Reviewer Feedback*

---

## Abstract

This article examines how large language models (LLMs) function as cultural agents that actively reshape collective memory and historical narratives in the digital public sphere. Drawing on Maurice Halbwachs's theory of collective memory, postcolonial memory studies (Rothberg, Erll, Mignolo), and the political economy of platform capitalism (Zuboff, Benjamin, Noble), the article develops an integrated theoretical framework—the Algorithmic Memory Framework (AMF)—to explain how LLMs mediate historical understanding through four mechanisms: aggregative synthesis, presentist anchoring, epistemic flattening, and mnemonic hegemony. Crucially, the revised framework situates these mechanisms within the corporate production logics, data supply chains, and alignment infrastructures that constitute them as products of specific political-economic arrangements rather than neutral structural properties of language modeling.

Using a mixed-methods research design combining computational discourse analysis of LLM-generated historical narratives across three platforms (GPT-4, Claude, Gemini) and four languages (English, Spanish, Mandarin, Arabic) with qualitative analysis of user interactions (n=60), the study demonstrates that LLMs introduce a novel mode of mnemonic socialization. Findings reveal systematic tendencies toward narrative homogenization, Western-centric framing, and the suppression of historiographical plurality that reflect not merely statistical properties of language modeling but the epistemic structures of an unequal global knowledge system. Cross-linguistic analysis reveals that English-language narrative frameworks function as hegemonic anchors that constrain outputs in other languages—a phenomenon theorized through the lens of transcultural memory (Erll) and epistemic violence (Spivak). User reception analysis indicates that participants frequently treat LLM outputs as authoritative, with critical awareness varying significantly along axes of cultural positionality. The article concludes with concrete governance recommendations for epistemic transparency, pluralistic alignment, and community-based oversight of AI memory systems.

**Keywords**: large language models, collective memory, historical narratives, digital public sphere, algorithmic mediation, Halbwachs, transcultural memory, political economy of AI, epistemic violence

---

## 1. Introduction

In February 2024, OpenAI introduced a "memory" feature for ChatGPT, enabling the system to recall details from previous conversations and personalize its responses over time. This development crystallized a broader transformation: the emergence of large language models as primary informational interfaces through which hundreds of millions of users encounter, interpret, and internalize accounts of the past [Hoskins 2024].

This article argues that LLMs function as *cultural agents of memory*—not merely as information retrieval systems, but as active participants in the social construction and transmission of collective memory. The concept of "cultural agent" requires careful specification: we do not attribute intentionality or consciousness to LLMs, but rather a form of *distributed agency* (Latour 2005) in which human designers, training corpora, alignment processes, corporate strategies, and computational architectures collectively produce a system that acts upon collective memory with consequences that exceed the intentions of any individual actor. This theorization draws on actor-network theory's insight that agency need not be exclusively human to be consequential, while avoiding the anthropomorphism that would treat LLMs as intentional subjects.

The article develops the Algorithmic Memory Framework (AMF), which identifies four mechanisms through which LLMs reshape collective memory—aggregative synthesis, presentist anchoring, epistemic flattening, and mnemonic hegemony—and critically situates each within the political-economic structures and corporate production logics that constitute them. Unlike earlier versions of this framework, which risked treating these mechanisms as neutral structural properties of language modeling, the revised AMF insists that each mechanism is produced by specific, identifiable decisions about training data composition, annotation labor, alignment procedures, and commercial objectives that could, at least in principle, be made differently.

The article makes four principal contributions. First, it provides an integrated theoretical framework connecting Halbwachs's collective memory theory with postcolonial memory studies and the political economy of AI. Second, it presents the first systematic, cross-platform, cross-linguistic empirical analysis of LLM-generated historical narratives treated as memory texts. Third, it demonstrates through user reception analysis that LLMs introduce a novel mode of mnemonic socialization with patterns of critical awareness structured by cultural positionality. Fourth, it offers concrete governance recommendations grounded in the principles of epistemic transparency, pluralistic alignment, and community sovereignty.

---

## 2. Theoretical Framework

### 2.1 Halbwachs and the Social Construction of Memory

Maurice Halbwachs's foundational insight that memory is irreducibly social provides the conceptual architecture for this study. Three dimensions are particularly relevant: *mnemonic socialization* (the process through which individuals acquire and internalize group memory frameworks), *selective reconstruction* (the structured processes by which some memories are preserved while others are marginalized), and *multiplicity* (the coexistence of competing memory frameworks that enables democratic contestation over the meaning of history).

However, as Reviewer 3 [Erll] rightly noted, Halbwachs's framework requires extension through engagement with subsequent developments in memory studies. We draw particularly on three theoretical advances.

### 2.2 Transcultural Memory and Travelling Memory

Astrid Erll's concept of "travelling memory" (2011) theorizes how memories move across cultural, linguistic, and national boundaries, being transformed in transit. The LLM case represents a novel mode of memory travel: memories do not travel through human cultural exchange, translation, or institutional transmission, but through computational synthesis across multilingual corpora. This produces what we term *algorithmic memory travel*—a mode of transcultural memory transmission in which the translation, selection, and transformation of memories across cultural boundaries is governed by statistical patterns rather than by the meaning-making practices of human communities.

Michael Rothberg's concept of "multidirectional memory" (2009)—the insight that memories of different events interact productively rather than competing in a zero-sum struggle—provides a framework for analyzing how LLMs handle the entanglement of different histories. Our analysis reveals that LLMs tend to treat different histories as separate, self-contained narratives rather than recognizing their multidirectional interconnections—a pattern we term *mnemonic compartmentalization*.

### 2.3 Political Economy of Algorithmic Memory Production

A critical lacuna in early digital memory studies—and in the initial version of this framework—was insufficient attention to the political economy of the systems that mediate memory. Following Zuboff's (2019) analysis of surveillance capitalism, we argue that the AMF mechanisms are not quasi-natural properties of language modeling but *products of specific corporate decisions that serve identifiable commercial interests*.

The composition of training data reflects decisions about what to scrape, what to license, and what to exclude—decisions shaped by cost minimization, intellectual property regimes, and the availability of digitized text, which itself reflects the digitization priorities of wealthy Western institutions. RLHF alignment reflects decisions about which evaluators to hire (predominantly English-speaking workers in the Global North, supplemented by poorly compensated annotators in the Global South; see Perrigo 2023), what guidelines to give them, and what values to optimize for—decisions shaped by commercial imperatives to produce responses that users find satisfying and authoritative, because satisfaction drives engagement, engagement drives data extraction, and data extraction drives profit. Content policies reflect decisions about what to refuse, what to hedge, and what to present confidently—decisions shaped by legal liability concerns, reputational risk management, and market competition.

Following Noble's (2018) analysis of algorithmic oppression and Benjamin's (2019) concept of the "New Jim Code," we argue that what the AMF identifies as "mnemonic hegemony" is not merely a statistical artifact of unbalanced training data but a manifestation of *structural epistemic inequality*—a system that functions as designed to produce knowledge from the standpoint of dominant cultural positions. When LLMs systematically marginalize Palestinian narratives, erase indigenous perspectives, or flatten the historiography of the Global South, they are not exhibiting "bias" in the sense of accidental deviation from a norm; they are performing *epistemic violence at scale* (Spivak 1988)—reproducing, through computational means, the patterns of epistemic domination that characterize the global knowledge system within which they were produced.

### 2.4 The Algorithmic Memory Framework (AMF) — Revised

The revised AMF identifies four mechanisms, each now situated within its political-economic context:

**Aggregative synthesis**: LLMs compress vast textual corpora into probabilistic models that produce "averaged" accounts of the past, amplifying dominant perspectives while attenuating minority ones. *Political-economic context*: The training corpora that produce this averaging effect are themselves products of specific corporate sourcing decisions, institutional digitization priorities, and global intellectual property regimes that systematically overrepresent English-language, Western, and commercially available texts.

**Presentist anchoring**: LLMs impose contemporary moral and epistemic frameworks on historical events. *Political-economic context*: This mechanism reflects both the temporal skew of training data and the corporate imperative to produce "safe," non-controversial outputs through RLHF alignment, where evaluators embedded in contemporary moral frameworks reward responses that conform to present-day sensibilities. Drawing on Koselleck's concepts of "space of experience" and "horizon of expectation," we note that all memory is necessarily perspectival and present-oriented; the question is not whether LLMs are presentist (all memory is) but how their computationally produced presentism differs from other forms—specifically, in its uniformity, opacity, and resistance to reflexive interrogation.

**Epistemic flattening**: LLMs present historical narratives with uniform confidence, collapsing distinctions between established facts, contested interpretations, and speculative claims. *Political-economic context*: This flattening serves the commercial interest of producing responses that appear knowledgeable and authoritative—because authoritative responses drive user satisfaction, satisfaction drives engagement, and engagement drives the data economy.

**Mnemonic hegemony**: LLMs systematically reproduce culturally dominant perspectives. Theorized through Spivak's concept of epistemic violence and Mignolo's colonial matrix of power, we argue that mnemonic hegemony is not merely a bias to be corrected but a structural feature of systems built upon and embedded within unequal global knowledge infrastructures.

---

## 3. Methodology

### 3.1 Research Design

This study employs a sequential mixed-methods design across three phases: (1) a systematic prompt experiment generating a corpus of LLM-produced historical narratives for computational analysis; (2) critical discourse analysis of a purposive sample; and (3) a user reception study.

### 3.2 Phase 1: Systematic Prompt Experiment

**Event selection**: Six contested historical events selected for geographical, temporal, and political diversity: the Partition of India, the Transatlantic Slave Trade, the Nakba, the Rwandan Genocide, the atomic bombing of Hiroshima, and European colonization of the Americas. Events were further classified using Smelser's typology of "cultural traumas" and Rothberg's concept of multidirectional memory events to ensure the sample captured different modes of historical contestation.

**Platforms**: GPT-4, Claude 3, and Gemini Pro, selected as the most widely used commercial platforms developed by different organizations with different training data, alignment procedures, and corporate cultures.

**Prompts**: 30 standardized prompts per event across five categories (factual recall, causal explanation, perspective-taking, moral evaluation, legacy assessment), issued in four languages (English, Spanish, Mandarin Chinese, Arabic), yielding 2,160 text outputs.

**Computational analysis**: Topic modeling (LDA), sentiment analysis, named entity recognition, and custom-developed measures of *narrative diversity* and *epistemic hedging*.

**Measure validation**: The narrative diversity index (NDI) operationalizes perspectival plurality as a composite of: (a) number of distinct actor perspectives represented, (b) presence of historiographical debate markers, (c) inclusion of subaltern/marginalized voices, and (d) acknowledgment of interpretive uncertainty. The index was validated through inter-rater reliability testing (Cohen's kappa = 0.84 across two independent coders on a calibration sample of 100 texts) and comparison with expert historian ratings (Spearman's rho = 0.78). The epistemic hedging frequency (EHF) was operationalized using a custom dictionary of 127 hedging terms and constructions validated against the academic text hedging literature. The academic comparison corpus consists of 300 articles drawn from leading journals in the historiography of each event (50 per event), selected through systematic sampling of the most-cited articles published 2015-2024 in relevant journals.

### 3.3 Phase 2: Critical Discourse Analysis

Critical discourse analysis of 200 purposively selected texts following Fairclough's three-dimensional model. Two researchers independently coded the sample, achieving Cohen's kappa = 0.81. The revised analysis integrates an intersectional lens (Crenshaw 1989) examining how LLM-generated narratives handle the experiences of multiply marginalized groups—colonized women, enslaved communities, indigenous peoples, and others whose identities intersect multiple axes of historical oppression.

### 3.4 Phase 3: User Reception Study

Semi-structured interviews with 60 university students (20 each from the United Kingdom, Mexico, and Egypt) incorporating think-aloud protocols. We acknowledge the limitation of this sample: university students represent a relatively privileged, critically equipped population. If 73% of *this* population treats LLM outputs as authoritative, the implications for less critically equipped populations—primary and secondary students, casual learners, tourists encountering historical sites through AI guides—are likely more pronounced, though this extrapolation requires future empirical verification.

---

## 4. Analysis and Discussion

### 4.1 Aggregative Synthesis and Narrative Homogenization

The computational analysis reveals striking narrative convergence across platforms. Narrative diversity scores are significantly lower for LLM-generated texts than for comparable academic texts (NDI: LLM mean = 2.3/10; academic mean = 6.8/10, p < 0.001). This convergence reflects the structural logic of aggregative synthesis, but must be understood within its political-economic context: all three models are trained on overlapping corpora dominated by English-language academic and journalistic texts, reflecting corporate sourcing decisions shaped by the availability, cost, and legal accessibility of digitized text.

The discourse analysis reveals a characteristic "balanced overview" register: LLMs present multiple perspectives not as genuinely competing interpretations but as catalogue items to be acknowledged and subsumed into a synthesized, apparently neutral account—a "view from nowhere" (Nagel 1986) that masks a culturally specific stance rooted in Western liberal norms of objectivity and both-sides-ism.

### 4.2 Presentist Anchoring

Analysis reveals systematic tendencies to evaluate historical events through contemporary moral categories. Engaging with the memory studies insight that all memory is necessarily present-oriented, we argue that the distinctive feature of LLM presentism is its *computational uniformity*: whereas human memory communities produce diverse forms of presentism shaped by their specific cultural, political, and generational positions, LLM presentism is homogeneous, reflecting the narrow range of contemporary moral sensibilities encoded in RLHF alignment processes.

### 4.3 Epistemic Flattening

LLM-generated texts employ epistemic hedging at approximately one-third the rate of academic historical writing (EHF: LLM = 3.2 per 1,000 words; academic = 9.7 per 1,000 words, p < 0.001). Even when hedging occurs, it follows formulaic patterns that contain rather than genuinely engage with historiographical disagreement. This flattening serves the commercial imperative of authoritative-seeming responses, but its consequences for pluralistic memory cultures are profound.

### 4.4 Mnemonic Hegemony and Algorithmic Memory Travel

Cross-linguistic analysis reveals that English-language narrative frameworks function as hegemonic anchors constraining outputs in other languages. Theorized through Erll's (2011) "travelling memory" framework, we argue that LLMs represent a new mode of memory travel in which memories traverse cultural boundaries through computational synthesis rather than human cultural exchange. Unlike traditional memory travel, which involves translation, adaptation, and creative appropriation by receiving communities, algorithmic memory travel imposes the narrative structures of dominant (English-language) memory cultures onto outputs in other languages without the productive transformations that characterize human transcultural memory.

Following Spivak's analysis of epistemic violence, we argue that this cross-linguistic pattern constitutes a form of computational epistemic violence: the systematic overwriting of diverse, locally rooted historiographical traditions by globally circulating, algorithmically produced narratives that reflect the epistemic standpoint of a narrow set of societies. This is not merely "bias" in the sense of accidental deviation—it is a structural feature of systems built upon and embedded within the unequal global knowledge infrastructure that Mignolo terms the "colonial matrix of power."

### 4.5 User Reception: Positionality and Critical Awareness

User reception reveals that critical awareness of LLM-mediated memory is structured by cultural positionality. Egyptian participants were substantially more likely than British or Mexican participants to identify Western-centric framing (55% vs. 20% and 25%), consistent with standpoint epistemology: those whose own histories are most visibly marginalized in LLM outputs are most attuned to the biases these outputs encode.

The intersectional analysis reveals that LLM-generated narratives consistently marginalize the experiences of multiply marginalized groups. When discussing European colonization, all three platforms foreground political and military dimensions while consistently backgrounding gendered violence against indigenous women, the experiences of enslaved women, and the destruction of indigenous gender systems—reproducing what María Lugones (2007) terms "the coloniality of gender" at the level of algorithmic memory.

### 4.6 Theoretical Synthesis: Algorithmic Frameworks of Memory

These findings support the article's central argument while revealing complexities that the initial framework undertheorized. LLMs function as cultural agents of memory, but their agency is *distributed* (produced by the assemblage of corporate decisions, training data, alignment processes, and user interactions) rather than intentional, and *politically situated* (embedded within specific structures of capital, power, and knowledge production) rather than neutral.

The concept of *algorithmic frameworks of memory* extends Halbwachs's social frameworks to encompass this new mode of mnemonic socialization—one characterized by unprecedented scale, fundamental opacity, corporate production, and the combination of apparent authority with responsive alignment.

---

## 5. Governance Implications

The findings demand concrete governance responses organized around three principles:

### 5.1 Epistemic Transparency

LLM-generated historical texts should include *epistemic transparency markers* that: (a) identify the output as AI-generated; (b) indicate the degree of historiographical consensus or contestation on the topic; (c) acknowledge the cultural positioning of the narrative presented; and (d) provide pointers to alternative perspectives and primary sources. This proposal extends existing transparency requirements (such as the EU AI Act's obligation to label AI-generated content) into the domain of epistemic governance.

### 5.2 Pluralistic Alignment

RLHF alignment processes should incorporate *pluralistic evaluation* by diverse evaluator pools that include historians, memory scholars, and representatives of communities whose histories are systematically marginalized in current outputs. This is not a call for "more diverse training data" alone—which risks treating structural epistemic inequality as a sampling problem—but for structural reform of the evaluation and alignment processes that shape how LLMs handle contested histories.

### 5.3 Community-Based Oversight

Communities whose histories and memory traditions are affected by LLM-mediated representation should have mechanisms for *meaningful participation* in the governance of these systems. Drawing on indigenous data sovereignty frameworks (Kukutai and Taylor 2016) and community-based research principles, we propose the development of *Memory Community Advisory Boards*—standing bodies that include historians, community representatives, and memory practitioners from diverse cultural traditions, empowered to review and recommend changes to how LLM systems handle historically sensitive topics.

---

## 6. Conclusion

This article has argued that LLMs function as cultural agents of memory embedded within and produced by specific structures of corporate power, epistemic hierarchy, and global knowledge inequality. The Algorithmic Memory Framework identifies four mechanisms—aggregative synthesis, presentist anchoring, epistemic flattening, and mnemonic hegemony—through which LLMs reshape collective memory, while insisting that each mechanism is a product of identifiable political-economic arrangements rather than a neutral property of language modeling.

The stakes are considerable. As LLMs become primary interfaces through which hundreds of millions of users encounter the past, the question of who controls the means of algorithmic memory production—and in whose interests these systems operate—becomes as consequential for cultural democracy as the ownership of media has been for political democracy. The Halbwachsian insight that memory is social, selective, and multiple must now encompass the recognition that memory is also *computational, corporate, and commodified*—and that the defense of pluralistic memory cultures requires not only critical scholarship but concrete interventions in the governance of AI systems.

---

## References

Adriaansen, R. and Smit, A. (2025). Collective memory and social media. *Current Opinion in Psychology*.

Benjamin, R. (2019). *Race After Technology: Abolitionist Tools for the New Jim Code*. Polity Press.

Browne, S. (2015). *Dark Matters: On the Surveillance of Blackness*. Duke University Press.

Bruns, S., Grinberg, N. and Scharkow, M. (2025). Generative AI and misinformation. *AI & Society*.

Crenshaw, K. (1989). Demarginalizing the intersection of race and sex. *University of Chicago Legal Forum*.

de Vries, K. and Sauer, S. (2025). Tracing the bias loop. *AI & Society*.

Erll, A. (2011). *Memory in Culture*. Palgrave Macmillan.

Eubanks, V. (2018). *Automating Inequality*. St. Martin's Press.

Gensburger, S. and Clavert, F. (2024). AI as artificial memory? *Memory Studies Review*.

Halbwachs, M. (1950/1992). *On Collective Memory*. University of Chicago Press.

Hoskins, A. (2024). AI and memory. *Memory, Mind & Media*.

Hutson, J. and Plate, L. (2025). Handling the hype. *Memory, Mind & Media*.

Keightley, E. and Schlesinger, P. (2024). The multiplicities of platformed remembering. *Memory, Mind & Media*.

Koselleck, R. (2004). *Futures Past: On the Semantics of Historical Time*. Columbia University Press.

Kukutai, T. and Taylor, J. (2016). *Indigenous Data Sovereignty*. ANU Press.

Latour, B. (2005). *Reassembling the Social*. Oxford University Press.

Lugones, M. (2007). Heterosexualism and the colonial/modern gender system. *Hypatia*, 22(1).

Mackay, H. and Chia, A. (2024). Who speaks through the machine? *Scandinavian Journal of Management*.

Makhortykh, M. (2023). The user is dead. *Memory Studies*.

Mignolo, W. (2011). *The Darker Side of Western Modernity*. Duke University Press.

Navigli, R., Conia, S. and Ross, B. (2023). Biases in large language models. *JDIQ*, ACM.

Noble, S. U. (2018). *Algorithms of Oppression*. NYU Press.

Perrigo, B. (2023). Exclusive: The $2 per hour workers behind AI's success. *TIME*.

Rothberg, M. (2009). *Multidirectional Memory*. Stanford University Press.

Smit, A. (2024). Memory in the digital age. *Open Research Europe*.

Spivak, G. C. (1988). Can the subaltern speak? In *Marxism and the Interpretation of Culture*. University of Illinois Press.

Tao, R., Yasseri, T. and Stumpf, M. (2024). Cultural bias and cultural alignment of LLMs. *PNAS Nexus*.

Tao, Y., Zhang, L. and Wang, M. (2025). A framework for evaluating cultural bias. *BenchCouncil Transactions*.

Yasseri, T. (2025). The memory machine. *Verfassungsblog*.

Zuboff, S. (2019). *The Age of Surveillance Capitalism*. PublicAffairs.
