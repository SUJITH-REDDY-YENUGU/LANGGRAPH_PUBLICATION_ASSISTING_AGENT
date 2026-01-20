from typing import TypedDict, Optional, List, Literal
from typing_extensions import Annotated

class ContentState(TypedDict):
    # Input-only: broadcast to all nodes, never updated
    raw_text: Annotated[str, "input"]

    # Outputs: each node writes only its own key
    title: Annotated[Optional[str], "output"]
    tldr: Annotated[Optional[str], "output"]
    tags: Annotated[Optional[List[str]], "output"]
    references: Annotated[Optional[List[str]], "output"]

    # Reviewer metadata
    review_status: Optional[Literal["approved", "revise"]]
    review_targets: Optional[List[Literal["title", "tldr", "tags", "references"]]]
    review_feedback: Optional[str]

    # Safety counter to prevent infinite loops
    revision_attempts: int
