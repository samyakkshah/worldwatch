from typing import List
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from utils.prompt import title_prompt

from models.chunk import Chunk

llm = OllamaLLM(model='llama3')

def generator(chunks: List[Chunk]) -> str:
    chunk_text = '\n'.join([chunk.text for chunk in chunks])
    prompt = title_prompt()
    chain = (prompt | llm | StrOutputParser())
    try:
        res = chain.invoke({"context": chunk_text})
        return res.strip()
    except Exception as e:
        print(f"Error generating summary: {e}")
        return "No Title generated"