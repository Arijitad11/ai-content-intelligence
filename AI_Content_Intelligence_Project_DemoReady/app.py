
import os
import sqlite3
from datetime import date, timedelta
import pandas as pd
import streamlit as st

try:
    from openai import OpenAI
except Exception:
    OpenAI = None

DB = "content_intelligence.db"
st.set_page_config(page_title="AI Content Intelligence", page_icon="✨", layout="wide")

def init_db():
    conn = sqlite3.connect(DB)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS content (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT, pillar TEXT, platform TEXT, format TEXT, status TEXT,
            priority TEXT, owner TEXT, deadline TEXT,
            views INTEGER DEFAULT 0, likes INTEGER DEFAULT 0, comments INTEGER DEFAULT 0,
            shares INTEGER DEFAULT 0, saves INTEGER DEFAULT 0, ctr REAL DEFAULT 0, notes TEXT
        )
    """)
    conn.commit(); conn.close()

def get_data():
    conn = sqlite3.connect(DB)
    df = pd.read_sql_query("SELECT * FROM content", conn)
    conn.close()
    return df

def add_item(row):
    conn = sqlite3.connect(DB)
    conn.execute("""INSERT INTO content
        (title,pillar,platform,format,status,priority,owner,deadline,views,likes,comments,shares,saves,ctr,notes)
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", row)
    conn.commit(); conn.close()

def ai_generate(prompt, system="You are an experienced AI content strategist and operations manager."):
    key = os.getenv("OPENAI_API_KEY")
    if not key or OpenAI is None:
        return None, "demo"
    try:
        client = OpenAI(api_key=key)
        response = client.responses.create(
            model=os.getenv("OPENAI_MODEL", "gpt-5-mini"),
            instructions=system,
            input=prompt,
        )
        return response.output_text, "ai"
    except Exception:
        # Billing/auth/network/API failures do not crash the portfolio demo.
        return None, "demo"

def demo_strategy(brand, product, audience, objective, platforms, tone):
    platform_text = " + ".join(platforms) if platforms else "Instagram"
    return f"""### Campaign strategy — {brand}

**Objective:** {objective}  
**Audience:** {audience}  
**Product/service:** {product}  
**Platforms:** {platform_text}  
**Tone:** {tone}

#### Content pillars
**1. Education** — Answer audience questions and explain the problem the product solves.  
**2. Product / Proof** — Demonstrate features, use cases, comparisons and outcomes.  
**3. Community / Storytelling** — Use customer stories and behind-the-scenes moments to humanize the brand.

#### 7-day content plan

| Day | Content idea | Pillar | Format | Hook | CTA | Priority | Effort |
|---|---|---|---|---|---|---|---|
| 1 | 3 common problems your audience faces | Education | Reel | "If you're still struggling with this..." | Save this | High | Low |
| 2 | Product/feature breakdown | Product / Proof | Carousel | "Here's what actually makes it different" | Comment your question | High | Medium |
| 3 | Customer problem → solution story | Community | Reel | "We kept hearing the same problem..." | Share with someone | High | Medium |
| 4 | Expert/founder insight | Trust | Post | "One thing most people misunderstand..." | Follow for more | Medium | Low |
| 5 | Quick checklist | Education | Carousel | "Before you buy, check these 5 things" | Save this checklist | High | Low |
| 6 | Behind the scenes | Community | Reel | "What goes into making this happen?" | Follow the journey | Medium | Medium |
| 7 | Weekly learning / recap | Education | Post | "7 things we learned this week" | Join the conversation | Medium | Low |

#### Operations recommendations
1. Prioritize high-impact, low-effort formats to maintain publishing consistency.
2. Assign every content item an owner and deadline before production starts.
3. Review performance weekly and feed the strongest patterns into the next campaign.
"""

def demo_insights(df):
    pub = df[df["views"] > 0].copy()
    pub["engagement_rate"] = ((pub.likes + pub.comments + pub.shares + pub.saves) / pub.views) * 100
    top = pub.sort_values("engagement_rate", ascending=False).iloc[0]
    pillar = pub.groupby("pillar", as_index=False)["engagement_rate"].mean().sort_values("engagement_rate", ascending=False)
    best = pillar.iloc[0]
    return f"""### AI optimization report — Demo Mode

**Top observed content:** **{top['title']}** has the highest observed engagement rate at **{top['engagement_rate']:.2f}%** in the demo dataset.

**Strongest content pillar:** **{best['pillar']}** has the highest average engagement rate at **{best['engagement_rate']:.2f}%**.

**Experiment to run next:** Create two variations of the strongest-performing hook while keeping the topic and format similar, then compare engagement and shares.

**Workflow recommendation:** Standardize briefing, scripting and review steps for high-performing formats to reduce production time.

**Next optimization cycle:** Add more published results and compare performance by platform, format, pillar and hook before making larger strategy changes.

> Demo Mode is available so the prototype can be demonstrated without an active API balance. When API access is available, the same workflow can use the LLM.
"""

init_db()

with st.sidebar:
    st.header("Prototype Mode")
    if os.getenv("OPENAI_API_KEY") and OpenAI is not None:
        st.success("API key detected")
        st.caption("If the API is unavailable or out of credits, the app automatically uses Demo Mode.")
    else:
        st.info("Demo Mode")
        st.caption("No API key is required to demonstrate the workflow.")
    st.markdown("**Workflow**")
    st.write("Strategy → Production → Analytics → Optimization")

st.title("✨ AI Content Intelligence & Campaign Operations")
st.caption("AI-led planning → production → analytics → optimization")

tabs = st.tabs(["Campaign Strategy", "Content Operations", "Performance Analytics", "AI Insights"])

with tabs[0]:
    st.subheader("Generate an AI-led campaign strategy")
    c1, c2 = st.columns(2)
    with c1:
        brand = st.text_input("Brand / project name", "NovaSkin")
        audience = st.text_input("Target audience", "18–30, urban, skincare-conscious")
        objective = st.selectbox("Campaign objective", ["Awareness", "Engagement", "Leads", "Conversions"])
    with c2:
        product = st.text_input("Product / service", "Affordable science-backed skincare")
        platforms = st.multiselect("Platforms", ["Instagram", "LinkedIn", "YouTube", "TikTok"], ["Instagram", "LinkedIn"])
        tone = st.selectbox("Tone", ["Educational", "Minimal", "Playful", "Premium", "Bold"])

    if st.button("Generate Strategy", type="primary"):
        prompt = f"""Create a practical 7-day content campaign for:
Brand: {brand}
Product/service: {product}
Audience: {audience}
Objective: {objective}
Platforms: {", ".join(platforms)}
Tone: {tone}

Return three content pillars with rationale and seven content ideas in a markdown table with:
Day, Title, Pillar, Platform, Format, Hook, CTA, Priority, Production Effort.
Then give three operational recommendations for a small content team."""
        result, mode = ai_generate(prompt)
        if result and mode == "ai":
            st.success("AI strategy generated successfully.")
            st.markdown(result)
        else:
            st.info("Demo Mode — showing the built-in strategy without using API credits.")
            st.markdown(demo_strategy(brand, product, audience, objective, platforms, tone))

with tabs[1]:
    st.subheader("Content production pipeline")
    with st.expander("Add a content item"):
        cols = st.columns(3)
        with cols[0]:
            title = st.text_input("Title")
            pillar = st.text_input("Content pillar", "Education")
            platform = st.selectbox("Platform", ["Instagram","LinkedIn","YouTube","TikTok"], key="op")
        with cols[1]:
            fmt = st.selectbox("Format", ["Reel","Carousel","Post","Short","Long-form video"], key="fmt")
            status = st.selectbox("Status", ["Idea","Script","Production","Editing","Review","Scheduled","Published"])
            priority = st.selectbox("Priority", ["High","Medium","Low"])
        with cols[2]:
            owner = st.text_input("Owner", "Me")
            deadline = st.date_input("Deadline", date.today() + timedelta(days=3))
            notes = st.text_input("Notes")
        if st.button("Add to pipeline"):
            if title.strip():
                add_item((title,pillar,platform,fmt,status,priority,owner,str(deadline),0,0,0,0,0,0,notes))
                st.success("Added.")
                st.rerun()

    df = get_data()
    if df.empty:
        st.info("No content items yet.")
        if st.button("Load demo pipeline"):
            demo_rows = [
                ("Myth-busting skincare","Education","Instagram","Reel","Published","High","Ava","2026-09-20",18400,1320,94,210,180,2.8,"Strong hook"),
                ("Ingredient breakdown","Education","Instagram","Carousel","Published","High","Ava","2026-09-21",9200,710,52,105,260,2.1,"High saves"),
                ("Founder story","Trust","LinkedIn","Post","Review","Medium","Arijita","2026-10-02",0,0,0,0,0,0,"Needs approval"),
                ("Behind the scenes","Community","Instagram","Reel","Production","Medium","Sam","2026-10-03",0,0,0,0,0,0,"Raw footage ready"),
            ]
            for r in demo_rows: add_item(r)
            st.rerun()
    else:
        st.dataframe(df.drop(columns=["id"]), use_container_width=True, hide_index=True)

with tabs[2]:
    st.subheader("Campaign performance")
    df = get_data()
    if df.empty:
        st.info("Add or load content data from the Content Operations tab.")
    else:
        published = df[df["views"] > 0].copy()
        if published.empty:
            st.info("Publish some content and add performance numbers to see analytics.")
        else:
            published["engagement_rate"] = ((published.likes + published.comments + published.shares + published.saves) / published.views) * 100
            a,b,c,d = st.columns(4)
            a.metric("Total views", f'{published.views.sum():,.0f}')
            b.metric("Engagement rate", f'{published.engagement_rate.mean():.2f}%')
            c.metric("Total shares", f'{published.shares.sum():,.0f}')
            d.metric("Total saves", f'{published.saves.sum():,.0f}')
            st.markdown("#### Content performance")
            st.dataframe(published[["title","platform","format","views","likes","comments","shares","saves","ctr","engagement_rate"]].sort_values("engagement_rate", ascending=False), use_container_width=True, hide_index=True)
            pillar = published.groupby("pillar", as_index=False).agg(views=("views","sum"), engagement_rate=("engagement_rate","mean")).sort_values("engagement_rate", ascending=False)
            st.markdown("#### Performance by content pillar")
            st.bar_chart(pillar.set_index("pillar")["engagement_rate"])

with tabs[3]:
    st.subheader("AI performance analyst")
    df = get_data()
    if df.empty or df["views"].sum() == 0:
        st.info("Load demo data or enter published performance data first.")
    else:
        if st.button("Generate optimization report", type="primary"):
            summary = df[df["views"] > 0].to_json(orient="records")
            prompt = f"""Analyze this content performance dataset:
{summary}

Act as a content operations analyst. Give:
- 3 evidence-based observations
- 3 content experiments to run next
- 3 workflow/production recommendations
- 3 things the team should stop or reduce
Do not invent numbers. Refer only to patterns present in the data."""
            result, mode = ai_generate(prompt)
            if result and mode == "ai":
                st.success("AI optimization report generated.")
                st.markdown(result)
            else:
                st.info("Demo Mode — showing built-in analysis without using API credits.")
                st.markdown(demo_insights(df))

st.divider()
st.caption("Portfolio MVP • AI + Operations + Analytics • Works with or without API credits")
