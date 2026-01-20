from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
import os

from graph.graph import build_graph
from graph.state import ContentState

app = FastAPI(title="Content Workflow")

class Output(BaseModel):
    title: str | None
    tldr: str | None
    tags: list[str] | None
    references: list[str] | None
    review_status: str | None
    review_targets: list[str] | None
    review_feedback: str | None

@app.post("/process", response_model=Output)
async def process_file(
    file: UploadFile = File(...),
    groq_api_key: str = Form(...)
):
    # Check file type
    if file.content_type not in ("text/plain",):
        raise HTTPException(status_code=400, detail="Only .txt files are supported")

    # Read file content
    text = (await file.read()).decode("utf-8", errors="ignore").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Empty file")

    # Build workflow
    workflow = build_graph(groq_api_key)

    # Initial state
    state: ContentState = {
        "raw_text": text,
        "title": None,
        "tldr": None,
        "tags": None,
        "references": None,
        "review_status": None,
        "review_targets": None,
        "review_feedback": None,
    }

    # Run workflow
    final_state = workflow.invoke(state, config={"recursion_limit": 10})


    return Output(
        title=final_state.get("title"),
        tldr=final_state.get("tldr"),
        tags=final_state.get("tags"),
        references=final_state.get("references"),
        review_status=final_state.get("review_status"),
        review_targets=final_state.get("review_targets"),
        review_feedback=final_state.get("review_feedback"),
    )

@app.get("/")
def root():
    return {"status": "ok", "message": "Upload a .txt file to /process with groq_api_key"}
