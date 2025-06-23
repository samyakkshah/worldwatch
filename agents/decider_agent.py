from collections import defaultdict
from typing import List, Tuple
from models.chunk import Chunk
from store.chunk_store import ChunkStore


def decider(chunks: List[Chunk], chunk_store: ChunkStore):
    narrative_score = defaultdict(float)
    narrative_count = defaultdict(int)
    for chunk in chunks:
        top_matches: List[Tuple[int, str]] = chunk_store.get_top_k_chunks(chunk)
        if not top_matches:
            return {"decision": "create"}

        for score, narrative_id in top_matches:
            narrative_score[narrative_id] += score
            narrative_count[narrative_id] += 1

    # Compute average similarity per narrative
    avg_scores = {
        nid: narrative_score[nid] / narrative_count[nid]
        for nid in narrative_score
    }

    # Choose best narrative
    best_nid, best_score = max(avg_scores.items(), key=lambda x: x[1])

    # Final decision
    if best_score >= 0.78:
        return {"decision": "attach", "narrative_id": best_nid, "score": best_score}
    else:
        return {"decision": "create"}