from typing import List, Dict, Any, Optional
from langgraph.graph import StateGraph, END

from agents.reporter_agent import reporter
from models.article import Article
from models.chunk import Chunk
from models.narrative import Narrative
from store.chunk_store import ChunkStore
from store.narrative_store import NarrativeStore
from .chunker import semantic_chunking
from .tagger import tagger

# Agents
from agents.decider_agent import decider
from agents import title_generator, summary_agent, story_text_agent

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
            "narrative_id": self.narrative_id,
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
    
    chunks = semantic_chunking(state.article.body, 50)
    print(f"Chunks created: {len(chunks)}")
    for chunk in chunks:
        state.current_chunks.append(tagger(chunk, state.article.article_id))
    return state.to_dict()

def decider_node(state_dict: Dict[str, Any]) -> Dict[str, Any]:
    state = FlowState.from_dict(state_dict)
    
    result = decider(state.current_chunks, state.chunk_store, state.narrative_store)
    state.decision = result['decision']
    print(f'Decision: {state.decision}')
    if result['decision'] == 'attach':
        state.narrative_id = result['narrative_id']
        narrative = state.narrative_store.get(state.narrative_id)
        if narrative is not None:
            print(f'Narrative Id: {state.narrative_id} \t Narrative Title: {narrative.title}')
        else:
            print(f'Narrative Id: {state.narrative_id} \t Narrative not found.')
    return state.to_dict()

def create_node(state_dict: Dict[str, Any]) -> Dict[str, Any]:
    state = FlowState.from_dict(state_dict)
    
    new_narrative = Narrative(state.current_chunks, state.article.source, state.article.article_id, state.article.image_url)
    state.narrative_store.add(new_narrative)
    for chunk in state.current_chunks:
        chunk.narrative_id = new_narrative.narrative_id
        state.chunk_store.add(chunk)
    state.narrative_id = new_narrative.narrative_id
    
    state.chunk_store.save('data/chunk_store.json')
    state.narrative_store.save('data/narrative_store.json')
    
    return state.to_dict()

def attach_node(state_dict: Dict[str, Any]) -> Dict[str, Any]:
    state = FlowState.from_dict(state_dict)
    
    state.narrative_store.update(state.narrative_id, state.current_chunks,state.article.source, state.article.article_id, state.article.image_url)
    for chunk in state.current_chunks:
        chunk.narrative_id = state.narrative_id
        state.chunk_store.add(chunk)

    state.chunk_store.save('data/chunk_store.json')
    state.narrative_store.save('data/narrative_store.json')
    
    return state.to_dict()

def title_node(state_dict: Dict[str, Any]) -> Dict[str, Any]:
    state = FlowState.from_dict(state_dict)

    if state.narrative_id:
        title = title_generator.generator(state.current_chunks)
        state.narrative_store.update_title(state.narrative_id, title)
        print(f"[title_node] Generate Title: {title}\n")
    
    state.narrative_store.save('data/narrative_store.json')
    return state.to_dict()

def story_node(state_dict: Dict[str, Any]) -> Dict[str, Any]:
    state = FlowState.from_dict(state_dict)

    if state.narrative_id:
        story_text = story_text_agent.generator(state.current_chunks)
        state.narrative_store.update_story_text(state.narrative_id, story_text)
        print(f"[story_node] Generated Story Text: {story_text}\n")
    
    state.narrative_store.save('data/narrative_store.json')
    return state.to_dict()

def summary_node(state_dict: Dict[str, Any]) -> Dict[str, Any]:
    state = FlowState.from_dict(state_dict)

    if state.narrative_id:
        summary = summary_agent.generator(state.current_chunks)
        state.narrative_store.update_summary(state.narrative_id, summary)
        print(f"[summary_node] Generated Summmary: {summary}\n")
    
    state.narrative_store.save('data/narrative_store.json')
    return state.to_dict()

def reporter_node(state_dict: Dict[str, Any]) -> Dict[str, Any]:
    state = FlowState.from_dict(state_dict)

    if state.narrative_id:
        narrative = state.narrative_store.get(state.narrative_id)
        if narrative:
            report_markdown = reporter(state.current_chunks, narrative)
            narrative.report = report_markdown  # Save in memory
            print(f"[reporter_node] Generated Report:\n{report_markdown[:300]}...\n")

    state.narrative_store.save('data/narrative_store.json')
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
    graph.add_node("title_node", title_node)
    graph.add_node("story_node", story_node)
    graph.add_node("summary_node", summary_node)
    graph.add_node("reporter_node", reporter_node)

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
    graph.add_edge("create_node", "title_node")
    graph.add_edge("attach_node", "title_node")
    graph.add_edge("title_node", "story_node")
    graph.add_edge("story_node", "summary_node")
    graph.add_edge("summary_node", "reporter_node")
    graph.add_edge("reporter_node", END)

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