from typing import List, Dict, Any
from langgraph.graph import StateGraph, END

from models.article import Article
from models.chunk import Chunk
from models.narrative import Narrative
from store.chunk_store import ChunkStore
from store.narrative_store import NarrativeStore
from .chunker import semantic_chunking
from .tagger import tagger
from agents.decider_agent import decider

class FlowState:
    def __init__(self, article: Article, chunk_store: ChunkStore, narrative_store: NarrativeStore):
        self.article: Article = article
        self.chunk_store = chunk_store
        self.current_chunks: List[Chunk] = []
        self.narrative_store = narrative_store
        self.decision: str = ''
        self.narrative_id: str = ''
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "article": self.article,
            "chunk_store": self.chunk_store,
            "current_chunks": self.current_chunks,
            "narrative_store": self.narrative_store,
            "decision": self.decision,
            "narrative_id": self.narrative_id
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'FlowState':
        """Create FlowState instance from dictionary"""
        state = cls.__new__(cls)  # Create instance without calling __init__
        state.article = data["article"]
        state.chunk_store = data["chunk_store"]
        state.current_chunks = data["current_chunks"]
        state.narrative_store = data["narrative_store"]
        state.decision = data["decision"]
        state.narrative_id = data["narrative_id"]
        return state

# Wrapper functions that handle dict <-> class conversion
def chunker_node(state_dict: Dict[str, Any]) -> Dict[str, Any]:
    state = FlowState.from_dict(state_dict)
    
    chunks = semantic_chunking(state.article.body, 100)
    for chunk in chunks:
        state.current_chunks.append(tagger(chunk, state.article.article_id))
    
    return state.to_dict()

def decider_node(state_dict: Dict[str, Any]) -> Dict[str, Any]:
    state = FlowState.from_dict(state_dict)
    
    result = decider(state.current_chunks, state.chunk_store)
    state.decision = result['decision']
    if result['decision'] == 'attach':
        state.narrative_id = result['narrative_id']
    
    return state.to_dict()

def create_node(state_dict: Dict[str, Any]) -> Dict[str, Any]:
    state = FlowState.from_dict(state_dict)
    
    new_narrative = Narrative(state.current_chunks, state.article.article_id)
    state.narrative_store.add(new_narrative)
    for chunk in state.current_chunks:
        chunk.narrative_id = new_narrative.narrative_id
        state.chunk_store.add(chunk)
    state.narrative_id = new_narrative.narrative_id
    
    return state.to_dict()

def attach_node(state_dict: Dict[str, Any]) -> Dict[str, Any]:
    state = FlowState.from_dict(state_dict)
    
    state.narrative_store.update(state.narrative_id, state.current_chunks, state.article.article_id)
    for chunk in state.current_chunks:
        chunk.narrative_id = state.narrative_id
        state.chunk_store.add(chunk)
    
    return state.to_dict()

def build_graph():
    # Define the state schema as a dict for LangGraph
    from typing import TypedDict
    
    class StateDict(TypedDict):
        article: Article
        chunk_store: ChunkStore
        current_chunks: List[Chunk]
        narrative_store: NarrativeStore
        decision: str
        narrative_id: str
    
    graph = StateGraph(StateDict)

    graph.add_node("chunker_node", chunker_node)
    graph.add_node("decider_node", decider_node)
    graph.add_node("create_node", create_node)
    graph.add_node("attach_node", attach_node)

    graph.set_entry_point("chunker_node")
    graph.add_edge("chunker_node", "decider_node")
    graph.add_conditional_edges(
        "decider_node",
        lambda state: state["decision"],
        {
            "create": "create_node",
            "attach": "attach_node"
        }
    )
    graph.add_edge("create_node", END)
    graph.add_edge("attach_node", END)

    return graph.compile()

def run_pipeline(article: Article, chunk_store: ChunkStore, narrative_store: NarrativeStore):
    # Create your class instance
    state = FlowState(article, chunk_store, narrative_store)
    
    # Convert to dict for LangGraph
    initial_state = state.to_dict()
    
    graph = build_graph()
    result = graph.invoke(initial_state)
    
    # Convert result back to class if needed
    return FlowState.from_dict(result)