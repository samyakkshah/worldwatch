from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from store.narrative_store import NarrativeStore
from store.chunk_store import ChunkStore
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to your frontend's URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],)


@app.get('/narratives')
def get_narratives():
    """
    Retrieve all narratives from the narrative store.
    """
    try:
        narrative_store = NarrativeStore()
        narrative_store.load('data/narrative_store.json')
        return JSONResponse(content={"narratives": narrative_store.to_dict()}, status_code=200)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@app.get("/narratives/{id}")
def get_narrative(id: str):
    """
    Retrieve a single narrative by its ID from the narrative store.
    """
    try:
        narrative_store = NarrativeStore()
        narrative_store.load('data/narrative_store.json')
        narrative = narrative_store.get(id)
        if narrative is not None:
            return JSONResponse(content={"narrative": narrative.to_dict()}, status_code=200)
        else:
            return JSONResponse(content={"error": "Narrative not found"}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
@app.get("/chunk/{id}")
def get_chunk_data(id: str):
    """
    Retrieve a single narrative by its ID from the narrative store.
    """
    try:
        chunk_store = ChunkStore()
        chunk_store.load('data/chunk_store.json')
        chunks = chunk_store.get(id)
        if chunks is not None:
            return JSONResponse(content={"chunk": chunks.to_dict()}, status_code=200)
        else:
            return JSONResponse(content={"error": "Narrative not found"}, status_code=404)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
    
