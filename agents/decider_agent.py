
from typing import List, Tuple
from models.chunk import Chunk
from store.chunk_store import ChunkStore
from store.narrative_store import NarrativeStore


def decider(chunks: List[Chunk], chunk_store: ChunkStore, narrative_store: NarrativeStore):
    from collections import defaultdict

    def topic_overlap_score(topics1, topics2):
        return len(set(topics1) & set(topics2)) / max(len(set(topics1) | set(topics2)), 1)



    narrative_score = defaultdict(float)
    narrative_count = defaultdict(int)
    for chunk in chunks:
        top_matches: List[Tuple[int, str]] = chunk_store.get_top_k_chunks(chunk)
        if not top_matches:
            return {"decision": "create"}

        for score, narrative_id in top_matches:
            topic_pool = []
            narrative = narrative_store.get(narrative_id)
            if narrative is not None and hasattr(narrative, "chunks") and narrative.chunks:
                for cid in narrative.chunks:
                    old_chunk = chunk_store.get(cid)
                    if old_chunk and hasattr(old_chunk, "topics"):
                        topic_pool.extend(old_chunk.topics)

            # ⬇ Compute topic overlap between this new chunk and the narrative's topics
            overlap = topic_overlap_score(chunk.topics, topic_pool)
            if overlap > 0.2:
                narrative_score[narrative_id] += score*(0.5+overlap)
                narrative_count[narrative_id] += 1

    # Compute average similarity per narrative
    avg_scores = {
        nid: narrative_score[nid] / narrative_count[nid]
        for nid in narrative_score
    }

    # Choose best narrative
    best_nid, best_score = max(avg_scores.items(), key=lambda x: x[1])

    # Final decision
    return {"decision": "attach", "narrative_id": best_nid, "score": best_score}