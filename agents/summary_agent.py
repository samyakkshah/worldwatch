from typing import List
from langchain_ollama import OllamaLLM
from langchain_core.output_parsers import StrOutputParser
from utils.prompt import summary_prompt

from models.chunk import Chunk

llm = OllamaLLM(model='llama3')

def generator(chunks: List[Chunk]) -> str:
    chunk_text = '\n'.join([chunk.text for chunk in chunks])
    prompt = summary_prompt()
    chain = (prompt | llm | StrOutputParser())
    try:
        res = chain.invoke({"context": chunk_text})
        return res.strip()
    except Exception as e:
        print(f"Error generating title: {e}")
        return "No Summary generated"