# Peer Review Report — Round 1

**Manuscript**: "Large Language Models as Cultural Agents: How AI-Generated Text Reshapes Collective Memory and Historical Narratives in the Digital Public Sphere"

**Journal**: *Memory Studies* (simulated review)

**Date**: 2026-03-09

---

## Reviewer 1: Shoshana Zuboff

**Affiliation**: Harvard Business School
**Expertise**: Surveillance capitalism, political economy of digital technologies, institutional transformation
**h-index**: ~42

### Scores

| Criterion | Score (1-10) | Comments |
|-----------|:---:|---------|
| Originality | 8 | The Algorithmic Memory Framework is a genuinely novel contribution that fills an important gap between collective memory theory and critical AI studies. The identification of four distinct mechanisms is analytically productive. |
| Theoretical Framework | 7 | The Halbwachsian foundation is well articulated, but the framework undertheorizes the political economy of LLM production. The corporate actors building these systems have specific commercial interests that shape what the paper treats as purely structural properties. |
| Methodology | 6 | The three-phase design is ambitious and appropriately mixed-methods. However, the prompt experiment raises reproducibility concerns given model versioning, and the user study sample (n=60) is modest for the scope of claims advanced. |
| Literature Engagement | 7 | Strong engagement with digital memory studies and recent AI scholarship. Conspicuous omission of the political economy literature on platform capitalism, data labor, and the commercial logics driving LLM development. |
| Argumentation & Evidence | 7 | The empirical findings are presented clearly and align well with the theoretical framework. The statistical comparisons (narrative diversity scores, hedging frequencies) are useful but would benefit from more methodological detail on how these measures were constructed and validated. |
| Clarity & Writing | 8 | Well-written, lucid prose. The paper reads as a mature scholarly contribution. Minor tendency toward over-long paragraphs in the analysis section. |
| Significance | 8 | This paper addresses one of the most consequential and underexamined dimensions of the LLM revolution. Its significance is substantial. |

**Overall Score**: 7.3 / 10

### Strengths

1. **Conceptual architecture**: The AMF provides a clear, analytically differentiated framework that other scholars can adopt, test, and extend. The four-mechanism structure avoids the vagueness that plagues much critical AI scholarship.

2. **Empirical scope**: The cross-platform, cross-linguistic, mixed-methods design is commendable and unusual in a field where most studies examine a single model or a single type of output. The inclusion of user reception data alongside computational analysis is a genuine strength.

3. **Theoretical bridging**: The paper successfully bridges memory studies, digital culture studies, and critical algorithm studies — three literatures that speak to the same phenomena but rarely speak to one another.

4. **Timeliness and relevance**: The paper addresses an urgent question with implications for democratic culture, historical literacy, and AI governance, and does so with scholarly rigor rather than polemic.

### Weaknesses

1. **Political economy blind spot**: The paper treats the mechanisms of aggregative synthesis, presentist anchoring, epistemic flattening, and mnemonic hegemony as if they were neutral structural properties of language modeling. They are not. They are products of specific corporate decisions — about training data composition, RLHF reward functions, content policies, and commercial objectives. The absence of any sustained engagement with the political economy of AI production is a significant gap. Who owns the means of memory production? Who profits from it? These questions are central to understanding what the paper describes, yet they go unasked.

2. **Insufficient attention to the data supply chain**: The training corpora that produce the biases the paper documents are themselves products of specific histories — the digitization priorities of Western institutions, the labor conditions of data annotators in the Global South, the intellectual property regimes that determine what text is available for scraping. The paper would benefit from situating its findings within this material infrastructure.

3. **User study limitations insufficiently addressed**: The paper acknowledges that its user sample consists of university students, but does not adequately grapple with the implications of this limitation. University students are among the most critically equipped users of information technologies. If 73% of *this* population treats LLM outputs as authoritative, the implications for less critically equipped populations are staggering — but the paper does not pursue this inference with sufficient force.

4. **Governance recommendations are underdeveloped**: The conclusion gestures toward implications for developers, educators, and policymakers, but offers no concrete governance proposals. Given the paper's empirical findings, more specific recommendations would strengthen the contribution.

### Detailed Comments

The manuscript makes a valuable contribution by providing the first integrated theoretical framework connecting Halbwachs's collective memory theory with the specific sociotechnical mechanisms of LLM text generation. The Algorithmic Memory Framework is well constructed, and the empirical work is admirably comprehensive. The paper demonstrates clearly that LLMs do not function as neutral information retrieval systems but as active agents of memory construction, and the cross-platform convergence findings are particularly striking.

However, I am troubled by what the paper does not say. The mechanisms it identifies — aggregative synthesis, presentist anchoring, epistemic flattening, mnemonic hegemony — are presented as quasi-natural properties of language modeling, as if they emerged spontaneously from the statistical structure of text. In reality, every one of these mechanisms is shaped by corporate decisions that could, at least in principle, be made differently. The composition of training data reflects decisions about what to scrape, what to license, and what to exclude. RLHF alignment reflects decisions about what evaluators to hire, what guidelines to give them, and what values to optimize for. Content policies reflect decisions about what to refuse, what to hedge, and what to present confidently. The paper would be significantly strengthened by integrating an analysis of these corporate production dynamics, drawing on work in the political economy of platforms and what I have termed "surveillance capitalism." The commercial imperative to produce responses that users find satisfying and authoritative — because satisfaction drives engagement, engagement drives data extraction, and data drives profit — is not incidental to the memory effects the paper documents; it is constitutive of them.

Additionally, while the methodology is ambitious, certain claims would benefit from more rigorous substantiation. The narrative diversity and epistemic hedging measures are central to the paper's empirical contribution, yet the paper provides little detail on how these were operationalized, validated, or normed against the comparison corpus of academic historical texts. How were "comparable" academic texts selected? How was the academic comparison corpus constructed to ensure it represents a meaningful baseline? These questions matter because the quantitative comparisons anchor several of the paper's strongest claims.

### Suggestions

1. Add a substantive section (or substantially expand Section 2.3) on the political economy of LLM production, situating the four AMF mechanisms within the corporate decision-making structures and commercial logics that produce them.

2. Provide detailed methodological appendices describing the operationalization and validation of the narrative diversity and epistemic hedging measures, including the construction of the academic comparison corpus.

3. Expand the governance implications in the conclusion with concrete, actionable proposals — for example, requirements for epistemic transparency markers in LLM-generated historical texts, or mechanisms for incorporating diverse historiographical traditions into training and alignment.

4. Address the implications of user reception findings for populations beyond university students, even if only speculatively. The finding that 73% of a critically equipped population treats LLM outputs as authoritative demands extrapolation.

### Decision: **Major Revision**

---

## Reviewer 2: Safiya Umoja Noble

**Affiliation**: University of California, Los Angeles (UCLA), Department of Information Studies
**Expertise**: Algorithmic discrimination, critical internet studies, race and digital media
**h-index**: ~28

### Scores

| Criterion | Score (1-10) | Comments |
|-----------|:---:|---------|
| Originality | 7 | The AMF is a useful contribution, but the core insight — that algorithmic systems reproduce and amplify existing power asymmetries — has been well established in critical algorithm studies. The paper's originality lies more in its application to memory studies than in the mechanisms it identifies. |
| Theoretical Framework | 6 | The Halbwachsian framing is productive but risks Eurocentrism. The paper builds a framework around a European theorist to analyze phenomena that disproportionately affect non-European communities, without adequately engaging postcolonial, decolonial, or Global South memory scholarship. |
| Methodology | 7 | The mixed-methods design is strong. The cross-linguistic analysis is a particular strength. However, the absence of any engagement with community-based or participatory research methods is notable — the people most affected by mnemonic hegemony are studied but not involved as knowledge producers. |
| Literature Engagement | 6 | Good engagement with recent digital memory and AI studies. Significant gaps in engagement with critical race theory, postcolonial theory, decolonial memory studies, and the robust literature on algorithmic oppression beyond the single Navigli et al. citation on bias. |
| Argumentation & Evidence | 7 | The argument is well structured and the evidence is compelling. The cross-linguistic findings are powerful. However, the paper could push harder on the implications of its own findings — the data suggests not just "bias" but structural epistemic violence, and the paper's analytical language does not fully rise to this level. |
| Clarity & Writing | 8 | Clear, well-organized, and professionally written. |
| Significance | 8 | Important contribution to an urgent question. The paper opens a productive research agenda. |

**Overall Score**: 7.0 / 10

### Strengths

1. **Cross-linguistic methodology**: The decision to analyze LLM outputs across four languages and compare their perspectival orientations is a genuine methodological contribution. The finding that English-language frameworks anchor outputs in other languages is powerful evidence of what the paper aptly calls "mnemonic hegemony."

2. **User reception component**: The inclusion of user reception analysis alongside computational analysis provides a crucial dimension that most studies of LLM bias lack. Understanding *how users engage with* biased outputs is as important as documenting the biases themselves.

3. **Integration across literatures**: The paper successfully connects AI studies, memory studies, and critical digital culture in a way that makes each more productive. The concept of "algorithmic memory texts" is analytically useful.

4. **Empirical rigor**: The three-phase design, the scale of the prompt experiment (2,160 outputs), and the inter-rater reliability reporting demonstrate a commitment to methodological rigor.

### Weaknesses

1. **Insufficient engagement with race, colonialism, and power**: The paper documents what amounts to a system of epistemic domination — English-language, Western, Global North narratives overwriting diverse local memory traditions — but analyzes it primarily through the neutral language of "bias," "asymmetry," and "hegemony" without adequately engaging the critical race, postcolonial, and decolonial literatures that have theorized these dynamics for decades. The concept of "mnemonic hegemony" would benefit from engagement with Gayatri Spivak's work on epistemic violence, Walter Mignolo's concept of the "colonial matrix of power," or Achille Mbembe's analysis of the postcolony's relationship to memory. The paper's theoretical framework is built around European thinkers (Halbwachs, Foucault, Nagel, Assmann) discussing phenomena that most acutely affect non-European communities.

2. **"Bias" framing is inadequate**: The paper consistently uses the language of "bias" to describe what its own findings reveal to be structural features of an unequal global knowledge system. "Bias" implies a deviation from a norm that could be corrected; what the paper describes is a system that functions as designed — to produce knowledge from the standpoint of dominant cultural positions. Reframing from "bias" to "structural epistemic inequality" or "algorithmic epistemic violence" would better capture the severity of the phenomena documented.

3. **Participatory deficit**: The user reception study positions Egyptian, Mexican, and British students as objects of study rather than as co-producers of knowledge. A more critically engaged methodology would involve communities affected by mnemonic hegemony not just as interview subjects but as participants in defining research questions, interpreting findings, and developing responses.

4. **Intersectionality absent**: The paper documents cross-linguistic and cross-national differences but does not examine how race, gender, class, and other axes of identity intersect in shaping both LLM outputs and user reception. How do LLMs narrate histories of gendered violence? How do they represent the experiences of colonized women, enslaved women, indigenous queer people? The paper's event-focused analysis misses these intersectional dimensions.

### Detailed Comments

This manuscript makes a welcome contribution by connecting the growing literature on LLM bias with the theoretically rich tradition of collective memory studies. The Algorithmic Memory Framework provides a useful vocabulary for analyzing how LLMs mediate historical understanding, and the empirical work — particularly the cross-linguistic analysis — generates findings of genuine significance. The documentation of English-language narrative frameworks anchoring outputs in other languages is an important empirical contribution that deserves wide attention.

My principal concern is that the paper's analytical framework is insufficiently attuned to the dimensions of power, race, and coloniality that are central to the phenomena it describes. The paper documents a system in which Western, English-language, Global North narratives systematically overwrite diverse local memory traditions — a finding that resonates deeply with decades of scholarship in postcolonial studies, critical race theory, and decolonial thought. Yet the paper engages with none of this work. Halbwachs, for all his contributions, theorized memory within the context of early twentieth-century French sociology; his framework was not designed to address the global asymmetries of epistemic power that the paper's findings reveal. Building the AMF exclusively on European theoretical foundations while documenting its effects on non-European communities reproduces, at the level of scholarship, something analogous to what the paper critiques at the level of technology.

Furthermore, I want to push the authors to reconsider their use of the term "bias." In my own work on algorithmic discrimination, I have argued that framing structural inequalities as "bias" risks trivializing them — suggesting they are accidental deviations that can be fixed with better training data or more representative annotation teams. What the paper documents is not a bug but a feature of systems built on unequal global knowledge infrastructures. The language of "bias" should be supplemented or replaced with language that captures the structural, systemic, and historically rooted character of the inequalities at work. When LLMs systematically marginalize Palestinian narratives, erase indigenous perspectives, or flatten the historiography of the Global South, they are not exhibiting "bias" — they are performing epistemic violence at scale.

### Suggestions

1. Integrate engagement with postcolonial memory studies (e.g., Rothberg's multidirectional memory, Erll's transcultural memory, Mignolo's epistemic disobedience) and critical race theory into the theoretical framework, particularly the concept of mnemonic hegemony.

2. Reframe the analytical language from "bias" to structural epistemic inequality or algorithmic epistemic violence where appropriate, while maintaining analytical precision about different types and degrees of representational harm.

3. Add an intersectional analysis examining how LLM-generated historical narratives handle the experiences of multiply marginalized groups (e.g., colonized women, enslaved communities, indigenous peoples).

4. Discuss the implications of the paper's findings for communities that are most directly harmed by mnemonic hegemony, and consider how future research might employ participatory or community-based methods.

5. Engage with the literature on algorithmic oppression more broadly (Benjamin 2019, Browne 2015, Eubanks 2018) to situate LLM-mediated memory within the wider landscape of algorithmic harm.

### Decision: **Major Revision**

---

## Reviewer 3: Astrid Erll

**Affiliation**: Goethe University Frankfurt, Department of English and American Studies
**Expertise**: Memory studies, transcultural memory, media and memory, travelling memory
**h-index**: ~30

### Scores

| Criterion | Score (1-10) | Comments |
|-----------|:---:|---------|
| Originality | 8 | The paper represents a genuinely original contribution to memory studies. The concept of "algorithmic frameworks of memory" as an extension of Halbwachs's social frameworks is theoretically productive and well argued. |
| Theoretical Framework | 8 | Excellent grounding in Halbwachs and strong engagement with contemporary digital memory scholarship. The AMF is well constructed. I would like to see more engagement with the "travelling memory" and "transcultural memory" paradigms, which are directly relevant to the cross-linguistic findings. |
| Methodology | 7 | The mixed-methods design is appropriate and well executed. The event selection is thoughtful and well justified. The computational measures are interesting but could be better grounded in existing content analysis methodologies from memory studies. |
| Literature Engagement | 7 | Strong on Halbwachs, digital memory, and AI studies. Could engage more with the broader memory studies canon — Aleida Assmann's work on canon and archive, Rothberg on multidirectional memory, Levy and Sznaider on cosmopolitan memory, and the extensive literature on memory and media. |
| Argumentation & Evidence | 8 | The argument is carefully constructed and the evidence is well presented. The progression from computational analysis through discourse analysis to user reception creates a compelling multi-layered account. |
| Clarity & Writing | 9 | Exceptionally well written for a paper bridging multiple disciplinary traditions. The theoretical expositions are clear and accessible without sacrificing precision. |
| Significance | 9 | This paper opens a major new research agenda for memory studies. The question of how AI systems reshape collective memory will be one of the defining questions for the field in the coming decade, and this paper provides the first serious theoretical and empirical foundation for addressing it. |

**Overall Score**: 8.0 / 10

### Strengths

1. **Theoretical sophistication**: The paper demonstrates a deep and nuanced understanding of Halbwachs's theory, going beyond the superficial invocations of "collective memory" that are common in digital studies. The three dimensions of Halbwachs's theory that the paper identifies as relevant (mnemonic socialization, selectivity and reconstruction, multiplicity) are well chosen and productively developed.

2. **The AMF as a generative framework**: The four mechanisms of the AMF are analytically clear, empirically grounded, and theoretically generative — they open productive lines of inquiry rather than closing them down. The framework has the potential to organize a substantial research program.

3. **Cross-linguistic findings**: The documentation of how English-language narrative frameworks anchor outputs in other languages is one of the paper's most important contributions. This finding connects to longstanding debates in memory studies about the geopolitics of memory and the dominance of certain mnemonic cultures in global discourse.

4. **Integration of user reception**: The inclusion of user reception data is crucial and all too rare in studies of digital memory technologies. Understanding that users treat LLM outputs as authoritative transforms the findings from abstract concerns about textual properties into concrete concerns about the social construction of historical understanding.

### Weaknesses

1. **Underengagement with memory studies canon**: While the paper's engagement with Halbwachs is excellent, it underengages with several strands of contemporary memory studies that are directly relevant to its argument. The concept of "transcultural memory" (Erll 2011; Bond and Rapson 2014) would help theorize the cross-linguistic dynamics the paper documents. Rothberg's (2009) "multidirectional memory" provides a framework for understanding how memories of different events interact — relevant to understanding how LLMs handle the entanglement of colonial, Holocaust, and postcolonial memory. Aleida Assmann's distinction between "canon" and "archive" in cultural memory maps productively onto the paper's distinction between foregrounded and marginalized narratives. Levy and Sznaider's work on "cosmopolitan memory" is relevant to the question of whether LLMs produce genuinely cosmopolitan or merely hegemonic forms of global memory.

2. **The temporal dimension is undertheorized**: The paper's concept of "presentist anchoring" is valuable, but it could be developed further through engagement with the extensive memory studies literature on temporality, including Koselleck's "space of experience" and "horizon of expectation," and the broader debate about presentism in historical thinking. The paper claims that LLMs impose contemporary moral frameworks on the past, but it does not fully reckon with the memory studies insight that all memory is necessarily perspectival and present-oriented — the question is not whether LLMs are presentist (all memory is) but *how* their presentism differs from other forms.

3. **Event selection rationale could be strengthened**: While the six events are well chosen for diversity, the paper could benefit from a more systematic justification drawing on existing typologies of memory events — for example, distinguishing between "founding traumas" (Smelser), "multidirectional" memory events (Rothberg), and events with different degrees of transnational resonance.

4. **The concept of "cultural agent" needs more precision**: The paper uses the term "cultural agent" to describe LLMs, but does not fully specify what kind of agency is being attributed. In memory studies, agency is typically associated with intentionality, reflexivity, and social embeddedness. In what sense do LLMs possess these qualities? The paper would benefit from a more careful theorization of non-human or distributed agency, drawing on work in actor-network theory (Latour) or material semiotics.

### Detailed Comments

This manuscript makes what I consider to be the most significant theoretical contribution to the question of AI and collective memory that I have encountered to date. The Algorithmic Memory Framework is thoughtfully constructed, the empirical work is comprehensive, and the paper's central argument — that LLMs function as cultural agents introducing a new mode of mnemonic socialization — is both compelling and consequential. I was particularly impressed by the paper's Halbwachsian grounding, which goes well beyond the surface-level invocations of "collective memory" that are unfortunately common in recent digital media scholarship. The authors clearly understand the theoretical tradition they are working within, and their extension of Halbwachs's "social frameworks" to "algorithmic frameworks" of memory is a genuinely productive conceptual move.

The cross-linguistic findings are among the paper's most important contributions and connect directly to debates about the geopolitics of memory that have animated the field in recent years. The demonstration that English-language narrative frameworks anchor outputs in other languages provides empirical substance to what has until now been a largely theoretical concern about the homogenization of global memory cultures. This finding deserves to be developed further, ideally in conversation with the literature on "travelling memory" (Erll 2011), which theorizes how memories move across cultural boundaries and are transformed in the process. The LLM case represents a novel and potentially consequential mode of memory travel — one in which memories travel not through human cultural exchange but through computational synthesis — and the paper would benefit from theorizing this novelty more explicitly.

My principal suggestions for revision concern the paper's engagement with the broader memory studies literature. The paper is admirably current in its engagement with recent AI and digital memory scholarship, but it could strengthen its contribution by connecting more explicitly to established theoretical debates within memory studies — particularly around transcultural memory, multidirectional memory, and the politics of temporality. These connections would not only enrich the theoretical framework but also demonstrate the paper's relevance to ongoing conversations within the discipline, increasing its potential impact.

### Suggestions

1. Engage with the concepts of "transcultural memory" and "travelling memory" to theorize the cross-linguistic dynamics documented in Section 4.4, considering how LLMs represent a new mode of memory travel with distinct properties.

2. Develop the concept of "presentist anchoring" in dialogue with memory studies scholarship on temporality (Koselleck, A. Assmann), specifying how LLM presentism differs from the inherent present-orientation of all collective memory.

3. Theorize the concept of "cultural agent" more precisely, specifying the type of agency being attributed to LLMs and engaging with work on non-human agency in actor-network theory or posthumanist theory.

4. Strengthen the event selection rationale by connecting to existing typologies of memory events in the literature.

5. Consider engaging with Rothberg's "multidirectional memory" to analyze how LLMs handle the interconnections between different histories of violence and suffering (e.g., how they relate colonialism, slavery, and genocide).

### Decision: **Minor Revision**

---

## Editor Synthesis

**Editor**: [Associate Editor, *Memory Studies*]

### Meta-Review

The three reviewers are in broad agreement that this manuscript makes a significant and timely contribution to the intersection of memory studies and critical AI scholarship. The Algorithmic Memory Framework (AMF) is recognized by all reviewers as an original and analytically productive contribution, and the mixed-methods empirical design is commended for its ambition and scope. All three reviewers recommend publication after revision, though they differ on the extent of revision required (one minor revision, two major revisions).

### Key Strengths (Consensus)

1. **The AMF is an original, well-constructed theoretical framework** that fills an important gap between collective memory theory and critical AI studies. All reviewers recognize its potential to organize future research.

2. **The cross-platform, cross-linguistic empirical design** is commended as comprehensive and methodologically rigorous. The cross-linguistic findings are identified by all reviewers as among the paper's most important contributions.

3. **The integration of user reception data** is praised as a crucial dimension that distinguishes this study from purely computational analyses of LLM bias.

4. **The paper is exceptionally well written**, with clear theoretical exposition and well-organized empirical presentation.

### Critical Issues Requiring Revision

1. **Political economy of LLM production** (Reviewer 1, strongly supported by Reviewer 2): The paper must integrate analysis of the corporate, commercial, and labor dynamics that produce the phenomena it documents. The four AMF mechanisms should be situated within the decision-making structures and profit motives of LLM-producing companies.

2. **Engagement with postcolonial, decolonial, and critical race perspectives** (Reviewer 2, supported by Reviewer 3): The paper's theoretical framework relies exclusively on European theorists while documenting phenomena that disproportionately affect non-European communities. The revised version must engage with postcolonial memory studies, critical race theory, and decolonial thought — particularly in the theorization of "mnemonic hegemony."

3. **Deeper engagement with the memory studies canon** (Reviewer 3, supported by Reviewer 2): The paper should engage with transcultural memory, multidirectional memory, cosmopolitan memory, and the temporal dynamics of memory to strengthen its contribution within memory studies.

4. **Methodological transparency** (Reviewer 1): The paper must provide more detail on the operationalization and validation of key computational measures (narrative diversity scores, epistemic hedging frequencies) and on the construction of the academic comparison corpus.

5. **Analytical language** (Reviewer 2): The paper should reconsider its use of "bias" language where its findings reveal structural epistemic inequalities, and more precisely theorize the concept of "cultural agent" (Reviewer 3).

### Revision Instructions

The authors are invited to submit a revised manuscript addressing the following:

1. **Required**: Integrate a political economy dimension into the theoretical framework and analysis, situating the AMF mechanisms within the corporate logics of LLM production.

2. **Required**: Engage substantively with postcolonial, decolonial, and critical race scholarship, particularly in theorizing mnemonic hegemony and interpreting the cross-linguistic findings. At minimum, engage with Rothberg (multidirectional memory), Spivak (epistemic violence), and the critical algorithm studies literature on algorithmic oppression (Benjamin, Browne, Eubanks).

3. **Required**: Expand engagement with memory studies scholarship on transcultural memory, temporality, and the politics of memory to strengthen the paper's disciplinary positioning.

4. **Required**: Provide methodological appendices or expanded method sections detailing the operationalization and validation of computational measures.

5. **Recommended**: Theorize the concept of "cultural agent" more precisely, specifying the type of agency attributed to LLMs.

6. **Recommended**: Strengthen the conclusion with more specific governance recommendations.

7. **Recommended**: Address the implications of user reception findings for populations beyond university students.

**Overall Decision: Major Revision (Revise and Resubmit)**

The editors are optimistic about this manuscript's potential and encourage the authors to undertake a thorough revision. The core contribution — the AMF and its empirical demonstration — is strong. The requested revisions aim to strengthen the theoretical foundations and broaden the analytical perspective, not to alter the paper's fundamental direction.
