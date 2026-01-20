from langgraph.graph import StateGraph, END
from .state import ContentState
from .nodes import (
    manager_node,
    title_node,
    tldr_node,
    tags_node,
    references_node,
    reviewer_node,
)

def build_graph(api_key: str):
    graph = StateGraph(ContentState)

    graph.add_node("manager", manager_node)
    graph.add_node("title", lambda s: title_node(s, api_key))
    graph.add_node("tldr", lambda s: tldr_node(s, api_key))
    graph.add_node("tags", lambda s: tags_node(s, api_key))
    graph.add_node("references", lambda s: references_node(s, api_key))
    graph.add_node("reviewer", lambda s: reviewer_node(s, api_key))

    graph.set_entry_point("manager")

    # Fan-out
    graph.add_edge("manager", "title")
    graph.add_edge("manager", "tldr")
    graph.add_edge("manager", "tags")
    graph.add_edge("manager", "references")

    # Fan-in
    graph.add_edge("title", "reviewer")
    graph.add_edge("tldr", "reviewer")
    graph.add_edge("tags", "reviewer")
    graph.add_edge("references", "reviewer")

    # Conditional loop: reviewer decides
    def review_decision(state: ContentState):
        if state["review_status"] == "approved":
            return END
        if state.get("review_targets"):
            # send back to the first target in the list
            return state["review_targets"][0]
        return "manager"

    graph.add_conditional_edges("reviewer", review_decision)

    return graph.compile()
