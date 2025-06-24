
from typing import List, Tuple
from models.chunk import Chunk
from store.chunk_store import ChunkStore
from store.narrative_store import NarrativeStore
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def decider(chunks: List[Chunk], chunk_store: ChunkStore, narrative_store: NarrativeStore, similar_chunks: List[List[Chunk]]):
    from collections import defaultdict

    def topic_overlap_score(topics1: dict, topics2: dict) -> float:
        flat1 = set([item for sublist in topics1.values() for item in sublist])
        flat2 = set([item for sublist in topics2.values() for item in sublist])
        if not flat1 or not flat2:
            return 0.0

        return len(flat1 & flat2) / len(flat1 | flat2)


    narrative_score = defaultdict(float)
    narrative_count = defaultdict(int)
    for idx, chunk in enumerate(chunks):
        for narrative in narrative_store.get_all():
            cos_sim = cosine_similarity(
                np.array([chunk.embedding]),
                np.array([narrative.embedding])
            )[0][0]
            overlap = topic_overlap_score(chunk.topics, narrative.topic if isinstance(narrative.topic, dict) else {})
            score = cos_sim + 0.2 * overlap
            if overlap > 0.2:
                narrative_score[narrative.narrative_id] += score
                narrative_count[narrative.narrative_id] += 1

    if not narrative_score:
        return {"decision": "create"}
    
    # Compute average similarity per narrative
    avg_scores = {
        nid: narrative_score[nid] / narrative_count[nid]
        for nid in narrative_score
    }

    # Choose best narrative
    best_nid, best_score = max(avg_scores.items(), key=lambda x: x[1])

    # Final decision
    return {"decision": "attach", "narrative_id": best_nid, "score": best_score}