
# AI Content Intelligence & Campaign Operations

A portfolio-ready MVP demonstrating how AI can support the full content lifecycle:

**Strategy → Ideas → Prioritization → Production → Publishing → Analytics → Optimization**

## Why this project exists

This is designed around an AI-led content operating model rather than a basic AI caption generator. It demonstrates the intersection of:

- AI / LLM workflows
- Content strategy
- Project and operations management
- Data analytics
- Performance optimization

## Features

### 1. Campaign Strategy
Enter a brand, audience, objective, platforms and tone. The app generates:
- Content pillars
- 7-day campaign ideas
- Hooks and CTAs
- Priority
- Production effort
- Team recommendations

### 2. Content Operations
A lightweight production pipeline tracks:
- Idea
- Script
- Production
- Editing
- Review
- Scheduled
- Published

Each item can have an owner, deadline, priority and notes.

### 3. Performance Analytics
Tracks:
- Views
- Likes
- Comments
- Shares
- Saves
- CTR
- Engagement rate

It also compares performance by content pillar.

### 4. AI Optimization
The AI analyst turns campaign performance into:
- Evidence-based observations
- Experiments
- Production recommendations
- Areas to reduce

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Optional AI mode:

```bash
# Windows PowerShell
$env:OPENAI_API_KEY="your_key"

# macOS/Linux
export OPENAI_API_KEY="your_key"
```

If no API key is supplied, the app still works using demo strategy/analysis.

## Suggested GitHub description

> AI-powered content intelligence and campaign operations platform that combines LLM strategy generation, content workflow management, performance analytics and optimization recommendations.

## Resume bullet

**AI-Led Content Intelligence & Campaign Operations Platform** — Built a Python/Streamlit system combining LLM-based campaign planning, content workflow management, engagement analytics and AI-driven optimization recommendations to create a closed-loop content operating system.
