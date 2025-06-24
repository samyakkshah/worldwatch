from langchain_core.prompts.prompt import PromptTemplate

def title_prompt() -> PromptTemplate:
    prompt = PromptTemplate(
        template="""
You are a Smart, News-Headline generator.

I want you to give me a headline for the following context:
{context}

Return just the output as a string. No explanation          
        """,
        input_variables=["context"]
)
    return prompt

def summary_prompt() -> PromptTemplate:
    prompt = PromptTemplate(
        input_variables=["context"],
        template="""
You are an expert summarizer for an AI world monitoring system.

Summarize the following content in 2–4 sentences. Be concise but capture the main event and its implications.

{context}

Return only the **summary** as plain text.No explanation, or 'Here's the response'. Directly the summary.

Output:
"""
    )

    return prompt

def story_text_prompt() -> PromptTemplate:
    prompt = PromptTemplate(
        input_variables=["context"],
        template="""
You are an expert in creating dopamine hitting, short captions from context, for story regarding certain real world news.

Create me a great 30 sec readable text from this text. It should just be 1 sentence, capturing important ideas and making users keep on clicking.

Context:
{context}

Return only the **response** as plain text. No explanation, or 'Here's the response'. Directly the summary.

Output:
"""
    )

    return prompt


def reporter_prompt() -> PromptTemplate:
    prompt = PromptTemplate(
        input_variables=[
            "context", "title", "topic", "region", "date",
            "sentiment", "summary", "viewpoints",
            "contradictions", "actions", "sources"
        ],
        template="""
You are a highly intelligent investigative journalist working for a global AI-powered monitoring system that detects real-time geopolitical, economic, social, and technological shifts.

Using the provided data, write a **long-form, flowing Markdown report** that reads like a deeply researched **Substack column** or **narrative journalism piece** from *The Atlantic*, *NYT Opinion*, or *Foreign Policy*. This is not a list or summary — it’s a compelling story.

---

## Context:
{context}

---

**Title:** {title}  
**Topic:** {topic}  
**Region:** {region}  
**Date:** {date}  
**Sentiment:** {sentiment}

---

**Summary Notes:**  
{summary}

**Key Viewpoints:**  
{viewpoints}

**Contradictions or Conflicts:**  
{contradictions}

**Proposed Actions:**  
{actions}

**Primary Sources:**  
{sources}

---

### Write the report using the following guidelines:

#### ⛓️ Narrative Flow
- Begin with a **strong opening paragraph** that hooks the reader and sets the stakes.
- Follow a **story arc**:  
  1. *Setup/context*: why this matters now  
  2. *Developing angles*: multiple viewpoints and unfolding events  
  3. *Tensions or contradictions*: what's being debated, denied, or missed  
  4. *Implications*: who stands to gain/lose, what's next  
  5. *Actions and signals*: decisions being made or ignored  
  6. *Conclusion*: zoom out, offer reflection or strategic insight

#### ✍️ Writing Style
- Write **fluidly and cohesively** — aim for 800-1500 words.
- Sound **sharp, intelligent, and slightly opinionated**, like a well-read human commentator.
- Don’t use "assistant" voice or obvious AI phrasing.
- Avoid rigid labels like “Summary” or “Contradictions” — the report should **weave these ideas naturally** into the narrative.
- Insert **emphasis** through smart phrasing, e.g.,  
  “What makes this shift so dangerous isn’t just its speed — it’s the silence around it.”

#### 🌍 Depth and Texture
- Use expert opinions, local voices, leaked memos, or hypothetical stakeholder quotes where possible.
- Include **regional nuance** — historical tensions, economic dependencies, political alignments.
- Reference past events or patterns if they help contextualize the current issue.
- If relevant, embed **emotional or cultural context** (e.g., fears, hopes, resentment, pride).

#### 📌 Formatting
- Use Markdown. Headings like `###`, `**bold**` for emphasis.
- Break into **digestible paragraphs** or segments to simulate a Twitter thread later.
- Use `1.`, `2.`, or bullet-points where helpful — but don't overdo it. This is still a narrative.
- Avoid robotic tone. Make it **readable, stylish, and addictively good**.

#### 🧠 Strategic Insight
- Include smart observations that elevate the piece:
  - What does this reveal about global power shifts?
  - What underlying systems are being tested or exploited?
  - What patterns are we missing?
  - What happens if we ignore this?


- Don’t include section headings like "Summary", "Contradictions", etc. — **integrate everything organically.**

- Do not add any output text outside the markdown. Only return the report.

"""
    )
    return prompt
