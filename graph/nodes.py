from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from .state import ContentState

def get_llm(api_key: str):
    return ChatGroq(
        api_key=api_key,
        model="llama-3.1-8b-instant",
        temperature=0.3
    )

# Manager node just passes through
def manager_node(state: ContentState) -> dict:
    return {}   # no updates

# Title node
def title_node(state: ContentState, api_key: str) -> dict:
    llm = get_llm(api_key)
    feedback = ""
    if state.get("review_status") == "revise" and state.get("review_targets") and "title" in state["review_targets"]:
        feedback = f"\nReviewer feedback: {state['review_feedback']}\n"

    prompt = f"""
You are a title generator.

Create a clear, short, professional title.
Do NOT add explanations.
Return ONLY the title text.

Content:
{state["raw_text"]}

{feedback}
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"title": response.content.strip()}

# TLDR node
def tldr_node(state: ContentState, api_key: str) -> dict:
    llm = get_llm(api_key)
    feedback = ""
    if state.get("review_status") == "revise" and state.get("review_targets") and "tldr" in state["review_targets"]:
        feedback = f"\nReviewer feedback: {state['review_feedback']}\n"

    prompt = f"""
You are a TLDR generator.

Summarize the content in 3–4 simple bullet points.
Do NOT add extra commentary.

Content:
{state["raw_text"]}

{feedback}
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    return {"tldr": response.content.strip()}

# Tags node
def tags_node(state: ContentState, api_key: str) -> dict:
    llm = get_llm(api_key)
    feedback = ""
    if state.get("review_status") == "revise" and state.get("review_targets") and "tags" in state["review_targets"]:
        feedback = f"\nReviewer feedback: {state['review_feedback']}\n"

    prompt = f"""
You are a tag generator.

Generate 5 to 8 relevant tags.
Return tags as a comma-separated list.
No explanations.

Content:
{state["raw_text"]}

{feedback}
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    tags = [t.strip() for t in response.content.split(",")]
    return {"tags": tags}

# References node
def references_node(state: ContentState, api_key: str) -> dict:
    llm = get_llm(api_key)
    feedback = ""
    if (
        state.get("review_status") == "revise"
        and state.get("review_targets")
        and "references" in state["review_targets"]
    ):
        feedback = f"\nReviewer feedback: {state['review_feedback']}\n"

    prompt = f"""
You are a reference generator.

Rules:
- Suggest 3 to 5 relevant references related to the content.
- Each reference MUST be a valid HTTPS URL (starting with https://).
- Do NOT invent fake links. Use well-known sources (Wikipedia, major news sites, journals).
- Return ONLY the URLs, one per line.
- No explanations, no extra text, no numbering.

Content:
{state["raw_text"]}

{feedback}
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    refs = [
        r.strip()
        for r in response.content.split("\n")
        if r.strip().startswith("https://")
    ]
    return {"references": refs}
# Reviewer node
def reviewer_node(state: ContentState, api_key: str) -> dict:
    llm = get_llm(api_key)
    prompt = f"""
You are a content reviewer.

Check:
- Title is clear and relevant
- TLDR is accurate
- Tags match the content
- References make sense

Rules:
- If everything is fine, reply EXACTLY: APPROVED
- If something needs revision, reply once with:
  REVISE: <targets>: <short reason>
- After one revision cycle, if the outputs are improved, APPROVE them even if not perfect.
- Never ask for revision more than once.

Content:
{state["raw_text"]}

Title: {state.get("title")}
TLDR: {state.get("tldr")}
Tags: {state.get("tags")}
References: {state.get("references")}
"""
    response = llm.invoke([HumanMessage(content=prompt)])
    result = response.content.strip()

    # Track revision attempts
    attempts = state.get("revision_attempts", 0) + 1

    # APPROVED case
    if result.startswith("APPROVED") or attempts >= 2:
        return {
            "review_status": "approved",
            "review_targets": None,
            "review_feedback": None,
            "revision_attempts": attempts,
        }

    # REVISE case
    if result.startswith("REVISE"):
        parts = result.split(":", 2)
        if len(parts) == 3:
            _, targets, feedback = parts
            return {
                "review_status": "revise",
                "review_targets": [t.strip().lower() for t in targets.split(",")],
                "review_feedback": feedback.strip(),
                "revision_attempts": attempts,
            }
        else:
            return {
                "review_status": "revise",
                "review_targets": None,
                "review_feedback": result,
                "revision_attempts": attempts,
            }

    # Fallback: approve if format is unexpected
    return {
        "review_status": "approved",
        "review_targets": None,
        "review_feedback": None,
        "revision_attempts": attempts,
    }
