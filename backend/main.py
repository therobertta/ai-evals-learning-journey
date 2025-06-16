from __future__ import annotations

"""FastAPI application entry-point for the recipe chatbot."""

import csv
import json
from pathlib import Path
from typing import Final, List, Dict, Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from backend.utils import get_agent_response  # noqa: WPS433 import from parent

# -----------------------------------------------------------------------------
# Application setup
# -----------------------------------------------------------------------------

APP_TITLE: Final[str] = "Recipe Chatbot"
app = FastAPI(title=APP_TITLE)

# Serve static assets (currently just the HTML) under `/static/*`.
STATIC_DIR = Path(__file__).parent.parent / "frontend"
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")


# -----------------------------------------------------------------------------
# Request / response models
# -----------------------------------------------------------------------------

class ChatMessage(BaseModel):
    """Schema for a single message in the chat history."""
    role: str = Field(..., description="Role of the message sender (system, user, or assistant).")
    content: str = Field(..., description="Content of the message.")

class ChatRequest(BaseModel):
    """Schema for incoming chat messages."""

    messages: List[ChatMessage] = Field(..., description="The entire conversation history.")


class ChatResponse(BaseModel):
    """Schema for the assistant's reply returned to the front-end."""

    messages: List[ChatMessage] = Field(..., description="The updated conversation history.")


class TraceData(BaseModel):
    """Schema for trace data."""
    id: str
    query: str
    response: str


class AnnotationData(BaseModel):
    """Schema for annotation data."""
    trace_id: str
    open_code_notes: str
    failure_modes: Dict[str, bool] = Field(default_factory=dict)


class AnnotationResponse(BaseModel):
    """Schema for annotation save response."""
    success: bool
    message: str


# -----------------------------------------------------------------------------
# Data loading and storage
# -----------------------------------------------------------------------------

# Load trace data
TRACE_DATA_PATH = Path(__file__).parent.parent / "homeworks" / "hw2" / "hw2_bot_traces_20250613.csv"
ANNOTATIONS_PATH = Path(__file__).parent.parent / "homeworks" / "hw2" / "annotations.json"

# Failure mode definitions
FAILURE_MODES = [
    "missing_serving_size",
    "overcomplicated_simple_recipes", 
    "inconsistent_time_estimates",
    "missing_dietary_restriction_info",
    "incomplete_ingredient_substitutions",
    "inconsistent_recipe_formatting",
    "missing_equipment_requirements",
    "inadequate_safety_information"
]

def load_trace_data() -> List[TraceData]:
    """Load trace data from CSV."""
    traces = []
    if TRACE_DATA_PATH.exists():
        with open(TRACE_DATA_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                traces.append(TraceData(
                    id=row['id'],
                    query=row['query'],
                    response=row['response']
                ))
    return traces

def load_annotations() -> Dict[str, Dict]:
    """Load existing annotations."""
    if ANNOTATIONS_PATH.exists():
        with open(ANNOTATIONS_PATH, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

def save_annotations(annotations: Dict[str, Dict]) -> None:
    """Save annotations to JSON file."""
    with open(ANNOTATIONS_PATH, 'w', encoding='utf-8') as f:
        json.dump(annotations, f, indent=2, ensure_ascii=False)

# -----------------------------------------------------------------------------
# Routes
# -----------------------------------------------------------------------------


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(payload: ChatRequest) -> ChatResponse:  # noqa: WPS430
    """Main conversational endpoint.

    It proxies the user's message list to the underlying agent and returns the updated list.
    """
    # Convert Pydantic models to simple dicts for the agent
    request_messages: List[Dict[str, str]] = [msg.model_dump() for msg in payload.messages]

    try:
        updated_messages_dicts = get_agent_response(request_messages)
    except Exception as exc:  # noqa: BLE001 broad; surface as HTTP 500
        # In production you would log the traceback here.
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        ) from exc

    # Convert dicts back to Pydantic models for the response
    response_messages: List[ChatMessage] = [ChatMessage(**msg) for msg in updated_messages_dicts]
    return ChatResponse(messages=response_messages)


@app.get("/", response_class=HTMLResponse)
async def index() -> HTMLResponse:  # noqa: WPS430
    """Serve the chat UI."""

    html_path = STATIC_DIR / "index.html"
    if not html_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Frontend not found. Did you forget to build it?",
        )

    return HTMLResponse(html_path.read_text(encoding="utf-8"))


@app.get("/coding", response_class=HTMLResponse)
async def coding_interface() -> HTMLResponse:  # noqa: WPS430
    """Serve the open coding annotation UI."""
    
    html_path = STATIC_DIR / "coding.html"
    if not html_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Coding interface not found.",
        )
    
    return HTMLResponse(html_path.read_text(encoding="utf-8"))


@app.get("/api/traces")
async def get_traces() -> List[TraceData]:  # noqa: WPS430
    """Get all trace data."""
    try:
        return load_trace_data()
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error loading trace data: {str(exc)}",
        ) from exc


@app.get("/api/traces/{trace_id}")
async def get_trace(trace_id: str) -> TraceData:  # noqa: WPS430
    """Get a specific trace by ID."""
    traces = load_trace_data()
    for trace in traces:
        if trace.id == trace_id:
            return trace
    
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Trace {trace_id} not found",
    )


@app.get("/api/annotations")
async def get_annotations() -> Dict[str, Dict]:  # noqa: WPS430
    """Get all annotations."""
    return load_annotations()


@app.get("/api/annotations/{trace_id}")
async def get_annotation(trace_id: str) -> Optional[Dict]:  # noqa: WPS430
    """Get annotation for a specific trace."""
    annotations = load_annotations()
    return annotations.get(trace_id)


@app.post("/api/annotations", response_model=AnnotationResponse)
async def save_annotation(annotation: AnnotationData) -> AnnotationResponse:  # noqa: WPS430
    """Save an annotation."""
    try:
        annotations = load_annotations()
        annotations[annotation.trace_id] = {
            "open_code_notes": annotation.open_code_notes,
            "failure_modes": annotation.failure_modes,
            "timestamp": json.dumps({"$date": {"$numberLong": str(int(__import__("time").time() * 1000))}}),
        }
        save_annotations(annotations)
        return AnnotationResponse(success=True, message="Annotation saved successfully")
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error saving annotation: {str(exc)}",
        ) from exc


@app.get("/api/progress")
async def get_progress() -> Dict[str, int]:  # noqa: WPS430
    """Get annotation progress."""
    traces = load_trace_data()
    annotations = load_annotations()
    
    total_traces = len(traces)
    completed_traces = len(annotations)
    
    return {
        "total": total_traces,
        "completed": completed_traces,
        "remaining": total_traces - completed_traces,
        "percentage": round((completed_traces / total_traces * 100) if total_traces > 0 else 0, 1)
    }


@app.get("/api/failure-modes")
async def get_failure_modes() -> List[str]:  # noqa: WPS430
    """Get list of failure mode identifiers."""
    return FAILURE_MODES


@app.get("/api/export-csv")
async def export_csv() -> HTMLResponse:  # noqa: WPS430
    """Export annotations to CSV format matching error analysis template."""
    try:
        traces = load_trace_data()
        annotations = load_annotations()
        
        # Create CSV content
        csv_content = ["Trace_ID,User_Query,Full_Bot_Trace_Summary,Open_Code_Notes," + ",".join(FAILURE_MODES)]
        
        for trace in traces:
            annotation = annotations.get(trace.id, {})
            
            # Create summary (first 100 chars of response)
            summary = trace.response[:100].replace('"', '""').replace('\n', ' ') + "..."
            
            # Get failure mode values (0 or 1)
            failure_values = []
            for mode in FAILURE_MODES:
                value = 1 if annotation.get("failure_modes", {}).get(mode, False) else 0
                failure_values.append(str(value))
            
            # Clean up fields for CSV
            query = trace.query.replace('"', '""').replace('\n', ' ')
            notes = annotation.get("open_code_notes", "").replace('"', '""').replace('\n', ' ')
            
            row = f'"{trace.id}","{query}","{summary}","{notes}",{",".join(failure_values)}'
            csv_content.append(row)
        
        csv_text = "\n".join(csv_content)
        
        return HTMLResponse(
            content=f'<pre>{csv_text}</pre><br><a href="data:text/csv;charset=utf-8,{csv_text}" download="error_analysis_results.csv">Download CSV</a>',
            media_type="text/html"
        )
        
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error exporting CSV: {str(exc)}",
        ) from exc 