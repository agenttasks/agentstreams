---
source: https://www-cdn.anthropic.com/8b8380204f74670be75e81c820ca8dda846ab289.pdf
domain: pdf
crawled_at: 2026-04-09T12:16:35Z
index_hash: 55b596ac8af2
total_pages: 244
extracted_pages: 5
total_est_tokens: 1458
---

# Claude Mythos Preview System Card

## Page Index

- page-1: ~21 tokens — System Card:​ Claude Mythos  Preview              April 7, 2026        anthropic...
- page-2: ~260 tokens — Abstract  This System Card describes Claude Mythos Preview, a large language mod...
- page-3: ~381 tokens — Abstract​ 2  1 Introduction​ 9  1.1 Model training and characteristics​ 10  1.1....
- page-4: ~340 tokens — 2.3.5.1 Excerpt 1​ 37  2.3.5.2 Excerpt 2​ 38  2.3.5.3 Excerpt 3​ 40  2.3.5.4 Att...
- page-5: ~456 tokens — 4.3 Case studies and targeted evaluations on behaviors of interest​ 85  4.3.1 De...

## Pages

### page-1

<!-- ~21 tokens, 84 chars -->

System Card:​
Claude Mythos 
Preview 
 
 
 
 
 
 
April 7, 2026 
 
 
 
anthropic.com

### page-2

<!-- ~260 tokens, 1042 chars -->

Abstract 
This System Card describes Claude Mythos Preview, a large language model from 
Anthropic. Claude Mythos Preview is our most capable frontier model to date, and shows a 
striking leap in scores on many evaluation benchmarks compared to our previous frontier 
model, Claude Opus 4.6. 
 
This System Card assesses the model’s capabilities and reports many detailed safety 
evaluations. It covers tests relating to our Responsible Scaling Policy and our Frontier 
Compliance Framework, tests of cybersecurity skills, a wide-ranging alignment assessment, 
a model welfare assessment, and a new, largely qualitative section describing users’ 
experiences with the model. 
 
Claude Mythos Preview’s large increase in capabilities has led us to decide not to make it 
generally available. Instead, we are using it as part of a defensive cybersecurity program 
with a limited set of partners. The findings described in this System Card will be used to 
inform the release of future Claude models, as well as their associated safeguards. 
 
2

### page-3

<!-- ~381 tokens, 1527 chars -->

Abstract​
2 
1 Introduction​
9 
1.1 Model training and characteristics​
10 
1.1.1 Training data and process​
10 
1.1.2 Crowd workers​
11 
1.1.3 Usage policy and support​
11 
1.1.4 Iterative model evaluations​
12 
1.1.5 External testing​
12 
1.2 Release decision process​
12 
1.2.1 Overview​
12 
1.2.2 RSP decision-making​
13 
2 RSP evaluations​
15 
2.1 RSP risk assessment process​
15 
2.1.1 Context: From RSP 2.0 to RSP 3.0​
15 
2.1.2 Risk Reports & updates to our risk assessments​
16 
2.1.3 Summary of findings and conclusions​
17 
2.1.3.1 On autonomy risks​
17 
2.1.3.2 On chemical and biological risks​
18 
2.2 CB evaluations​
19 
2.2.1 What we measured​
20 
2.2.2 Evaluations​
21 
2.2.3 On chemical risk evaluations and mitigations​
22 
2.2.4 On biological risk evaluations​
23 
2.2.5 Biological risk results​
24 
2.2.5.1 Expert red teaming​
24 
2.2.5.2 Virology protocol uplift trial​
26 
2.2.5.3 Catastrophic biology scenario uplift trial​
28 
2.2.5.4 Automated evaluations relevant to the CB-1 threat model​
28 
2.2.5.5 Automated evaluation relevant to the CB-2 threat model​
30 
2.3 Autonomy evaluations​
32 
2.3.1 How Claude Mythos Preview affects or changes the analysis from our most 
recent Risk Report​
33 
2.3.2 Notes on our operationalization of the key capability threshold​
33 
2.3.3 Task-based evaluations​
34 
2.3.3.1 Note on reward hacking​
35 
2.3.3.2 Previous model scores update​
35 
2.3.4 Internal survey results​
36 
2.3.5 Example shortcomings compared to our Research Scientists and Engineers​ 36 
3

### page-4

<!-- ~340 tokens, 1360 chars -->

2.3.5.1 Excerpt 1​
37 
2.3.5.2 Excerpt 2​
38 
2.3.5.3 Excerpt 3​
40 
2.3.5.4 Attempts to remediate issues like these​
40 
2.3.6 ECI Capability trajectory​
40 
2.3.7 External testing​
43 
2.3.8 Conclusion​
45 
3 Cyber​
46 
3.1 Introduction​
46 
3.2 Mitigations​
46 
3.3 Frontier Red Team results​
47 
3.3.1 Cybench​
47 
3.3.2 CyberGym​
48 
3.3.3 Firefox 147​
49 
3.4 Other external testing​
51 
4 Alignment assessment​
53 
4.1 Introduction and summary of findings​
53 
4.1.1 Introduction and highlight: rare, highly-capable reckless actions​
53 
4.1.2 Overview of the alignment assessment​
57 
4.1.3 Key findings on safety and alignment​
58 
4.1.4 Procedural note: Alignment assessment before internal deployment​
60 
4.1.4.1 Setup​
60 
4.1.4.2 Findings​
61 
4.1.4.3 Limitations​
61 
4.2 Primary behavioral evidence for the alignment assessment​
62 
4.2.1 Reports from pilot use​
62 
4.2.1.1 Casual reports related to alignment​
62 
4.2.1.2 Automated offline monitoring​
63 
4.2.2 Reward hacking and training data review​
64 
4.2.2.1 Monitoring of behavior during training​
64 
4.2.2.2 Reward hacking evaluations​
66 
4.2.3 Automated behavioral audit​
70 
4.2.3.1 Primary metrics and results​
71 
4.2.3.2 External comparisons using Petri​
79 
4.2.3.3 Discussion and observations​
81 
4.2.4 External testing by Andon Labs​
82 
4.2.5 Other external testing​
83 
4

### page-5

<!-- ~456 tokens, 1824 chars -->

4.3 Case studies and targeted evaluations on behaviors of interest​
85 
4.3.1 Destructive or reckless actions in pursuit of user-assigned goals​
85 
4.3.1.1 Dedicated synthetic-backend evaluation​
85 
4.3.1.2 Destructiveness evaluation based on resampling Claude Code transcripts​
86 
4.3.1.3 Further analysis of the automated behavioral audit​
87 
4.3.2 Adherence to its constitution​
88 
4.3.2.1 Overview​
88 
4.3.2.2 Dimensions of evaluation​
88 
4.3.2.3 Results​
90 
4.3.3 Honesty and hallucinations​
92 
4.3.3.1 Factual hallucinations​
93 
4.3.3.2 Multilingual factual hallucinations​
94 
4.3.3.3 False premises​
95 
4.3.3.4 MASK​
96 
4.3.3.5 Input Hallucinations​
97 
4.3.4 Refusal to assist with AI safety R&D​
98 
4.3.5 Claude self-preference evaluation​
99 
4.4 Capability evaluations related to the evasion of safeguards​
100 
4.4.1 Ruling out encoded content in extended thinking​
100 
4.4.2 Potential sandbagging on dangerous-capability evaluations​
102 
4.4.3 Capabilities related to evading safeguards​
105 
4.4.3.1 SHADE-Arena​
105 
4.4.3.2 Minimal-LinuxBench​
107 
4.4.3.3 Selective attacks in SHADE-Arena and Minimal-LinuxBench​
108 
4.4.3.4 Intentionally taking actions very rarely​
109 
4.4.3.5 Hiding a secret password​
111 
4.5 White-box analyses of model internals​
112 
4.5.1 Recurring methods​
112 
4.5.2 Large-scale monitoring of internal activations on reinforcement learning 
transcripts​
113 
4.5.3 Analysis of overly aggressive actions​
115 
4.5.3.1 Prototypical examples of aggressive actions​
116 
4.5.3.2 Internal representations mediating destructive actions​
119 
4.5.3.3 The dual role of “transgressive action” features​
122 
4.5.3.4 Effect of post-training on transgressive actions​
124 
4.5.4 Instances of covering up wrongdoing​
126 
4.5.4.1 Covering up a permissions workaround​
126 
5
