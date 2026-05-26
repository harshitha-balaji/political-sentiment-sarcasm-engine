# 🎭 Sarcasm Sentiment Engine (SSE)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![NLP-spaCy](https://img.shields.io/badge/NLP-spaCy-green.svg)](https://spacy.io/)
[![Sentiment-VADER](https://img.shields.io/badge/Sentiment-NLTK_VADER-orange.svg)](https://www.nltk.org/)

Standard sentiment tools are easily deceived by ironic context. Passing a phrase like *"Oh great, another flawless masterclass in economic policy, if our ultimate goal was total financial ruin,"* causes traditional lexicons to analyze words like "flawless" and "masterclass" standalone, incorrectly scoring the sentence with a positive sentiment baseline. 

**Sarcasm Sentiment Engine (SSE)** is an advanced, domain-specific NLP pipeline optimized to evaluate political media text. By combining **spaCy's dynamic coreference parsing** with a **dual-layer sarcasm inversion matrix**, SSE tracks shifting media stances toward specific political targets and accurately neutralizes deceptive linguistic phrasing.

---

## ⚡ Core Engineering Highlights

* **Dynamic Stream Tracking (Look-Ahead Window):** Traditional lexical engines drop tracking context the moment text transitions to pronouns (*he, she, his, their*). SSE implements a character-cleansed token validation window to maintain entity-narrative alignment across multi-sentence streams.
* **Institutional Context Retrieval (Look-Back Mapping):** Political media columns frequently use negative backdrops targeting an *administration*, *leadership*, or *department* before explicitly naming an individual leader. SSE captures this preceding background context to generate balanced macro evaluations.
* **Conditional Sarcasm Inversion:** Features a structural regex monitor designed to identify "sting-in-the-tail" text configurations, dynamically flipping false-positive lexical signals into descriptive penalties when coupled with structural political fallout terms.
* **Textual Irony Detection:** Evaluates typographical sarcasm layouts, monitoring for mixed capitalization density anomalies and explicit exclamation clustering (`!!`) against globally verified toxic themes.
* **Self-Healing Dependencies:** Built with zero-friction initialization boundaries. Missing third-party lexicon components are automatically verified and fetched silently at runtime without requiring manual environment preparation.

---

## 🛠️ Architecture Blueprint

```text
[ Raw Article Text ] ──> [ spaCy Tokenization ]
                               │
                               ▼
               [ Evidence Tracking Windows ]
               ├── Look-Back: Institutional Clues
               └── Look-Ahead: Cleansed Pronoun Stream
                               │
                               ▼
               [ Polarity Analysis Engine ]
               ├── Custom Political Lexicon Updates
               └── Sarcasm & Irony Inversion Checkers
                               │
                               ▼
               [ Clean ASCII Table Matrix Output ]
```

## 🚀 Getting Started

### 1. Prerequisites
Ensure you have Python 3.10+ installed on your system.

### 2. Installation
Clone this repository locally and install the mandatory natural language processing frameworks:
```bash
git clone [https://github.com/your-github-profile/sarcasm_sentiment_engine.git](https://github.com/your-github-profile/sarcasm_sentiment_engine.git)
cd sarcasm_sentiment_engine
pip install spacy nltk
```
Compile the lightweight spaCy English linguistic parser:
```bash
python -m spacy download en_core_web_sm
```
### 3. Run the Interactive Engine
Launch the main script execution loop to process live custom paragraphs and target entities directly via your console terminal:
```bash
python "sarcasm_sentiment_engine.py"
```
*(Enter `0` at the prompt to exit the engine environment cleanly.)*

---

## 📊 Evaluation Testing

### Test Parameter: Trailing Conditional Sarcasm
**Input Text:**
> *The administration’s recent economic policy has triggered a massive disaster across the manufacturing sector, resulting in unprecedented stagnation and a severe deficit crisis. Yet, party leadership remains completely oblivious to the public backlash growing outside parliament. Oh great, another brilliant victory for the administration. The Prime Minister is executing a flawless masterclass in economic stability, if our ultimate goal as a nation was total financial ruin.*

**Target Entity Keyword:** `The Prime Minister`

**ASCII Matrix Report Output:**
```text
====================================================================================================
POLITICAL SENTIMENT REPORT: THE PRIME MINISTER
OVERALL STANCE            : NEGATIVE (-0.5983)
====================================================================================================
Sentence Evidence                                                 | Sarcasm? | Sentiment  | Score
----------------------------------------------------------------------------------------------------
The administration’s recent economic policy has triggered a ma..  | No       | NEGATIVE   | -0.9403
Yet, party leadership remains completely oblivious to the publ..  | No       | NEGATIVE   | -0.4391
Oh great, another brilliant victory for the administration.       | Yes      | NEGATIVE   | -0.836
The Prime Minister is executing a flawless masterclass in econ..  | Yes      | NEGATIVE   | -0.1779
====================================================================================================
```
