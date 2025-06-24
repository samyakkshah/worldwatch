from typing import List
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from models.chunk import Chunk
from utils.prompt import story_text_prompt
from models.narrative import Narrative
from datetime import datetime

llm = OllamaLLM(model='llama3')  # Consistent with your summary agent


def generator(chunks: List[Chunk]) -> str:
    chunk_text = '\n'.join([chunk.text for chunk in chunks])
    prompt = story_text_prompt()
    chain = (prompt | llm | StrOutputParser())
    try:
        res = chain.invoke({"context": chunk_text})
        return res.strip()
    except Exception as e:
        print(f"Error generating title: {e}")
        return "No Summary generated"
