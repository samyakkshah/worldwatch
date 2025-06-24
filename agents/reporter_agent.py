from typing import List
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from models.chunk import Chunk
from utils.prompt import reporter_prompt
from models.narrative import Narrative
from datetime import datetime

llm = OllamaLLM(model='llama3')  # Consistent with your summary agent

def reporter(chunks: List[Chunk], narrative: Narrative) -> str:
    prompt = reporter_prompt()
    chunk_text = '\n'.join([chunk.text for chunk in chunks])
    # Prepare values
    inputs = {
        "context": chunk_text,
        "title": narrative.title or "Untitled",
        "topic": narrative.topic or "Unknown",
        "region": "Unknown",  # You can later extend Narrative to include region
        "date": datetime.fromisoformat(narrative.created_at).strftime('%B %d, %Y'),
        "sentiment": f"{narrative.sentiment_trend:.2f}",
        "summary": narrative.summary,
        "viewpoints": narrative.view_points if narrative.view_points != "pending" else "Not yet available.",
        "contradictions": "None reported.",  # Placeholder
        "actions": "No actions yet recorded.",
        "sources": '\n'.join(narrative.sources)
    }

    chain = prompt | llm | StrOutputParser()

    try:
        return chain.invoke(inputs).strip()
    except Exception as e:
        print(f"Error in reporter agent: {e}")
        return "Report could not be generated."
