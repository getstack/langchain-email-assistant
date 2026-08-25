"""LangGraph multi-step communication workflow."""

from __future__ import annotations

from typing import Literal, TypedDict

from langchain_core.output_parsers import StrOutputParser
from langgraph.graph import END, StateGraph

from llm import get_model
from prompts import review_prompt
from rag import retrieve_context
from services.ask_service import ask_ai
from services.email_service import generate_email
from services.reply_service import generate_reply


class WorkflowState(TypedDict, total=False):
    mode: str
    notes: str
    tone: str
    length: str
    original_email: str
    context: str
    draft: str
    result: dict
    reviewed: bool


def understand_request(state: WorkflowState) -> WorkflowState:
    mode = state.get("mode", "write")
    return {**state, "mode": mode}


def retrieve_if_needed(state: WorkflowState) -> WorkflowState:
    if state.get("mode") != "ask":
        return {**state, "context": ""}
    context = retrieve_context(state.get("notes", ""))
    return {**state, "context": context}


def generate_response(state: WorkflowState) -> WorkflowState:
    mode = state.get("mode", "write")
    tone = state.get("tone", "Professional")
    length = state.get("length", "Medium")
    notes = state.get("notes", "")

    if mode == "reply":
        result = generate_reply(
            original_email=state.get("original_email", ""),
            notes=notes,
            tone=tone,
            length=length,
        )
    elif mode == "ask":
        result = ask_ai(
            question=notes,
            tone=tone,
            length=length,
            context=state.get("context", ""),
        )
    else:
        result = generate_email(notes=notes, tone=tone, length=length)

    return {**state, "result": result, "draft": result["text"]}


def review_draft(state: WorkflowState) -> WorkflowState:
    draft = state.get("draft", "")
    tone = state.get("tone", "Professional")
    chain = review_prompt | get_model(temperature=0.2) | StrOutputParser()
    reviewed_text = chain.invoke({"draft": draft, "tone": tone}).strip()

    result = dict(state.get("result") or {})
    if reviewed_text and reviewed_text != draft:
        # Keep email JSON shape if present; otherwise replace text.
        if result.get("feature") in {"write_email", "reply_email"} and "Subject:" in reviewed_text:
            result["text"] = reviewed_text
            result["body"] = reviewed_text
        else:
            result["text"] = reviewed_text
            result["body"] = reviewed_text
    return {**state, "result": result, "draft": result.get("text", draft), "reviewed": True}


def route_after_understand(state: WorkflowState) -> Literal["retrieve", "generate"]:
    if state.get("mode") == "ask":
        return "retrieve"
    return "generate"


def build_graph():
    graph = StateGraph(WorkflowState)
    graph.add_node("understand", understand_request)
    graph.add_node("retrieve", retrieve_if_needed)
    graph.add_node("generate", generate_response)
    graph.add_node("review", review_draft)

    graph.set_entry_point("understand")
    graph.add_conditional_edges(
        "understand",
        route_after_understand,
        {"retrieve": "retrieve", "generate": "generate"},
    )
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", "review")
    graph.add_edge("review", END)
    return graph.compile()


_APP = None


def run_workflow(
    *,
    mode: str,
    notes: str,
    tone: str,
    length: str,
    original_email: str = "",
) -> dict:
    global _APP
    if _APP is None:
        _APP = build_graph()
    final_state = _APP.invoke(
        {
            "mode": mode,
            "notes": notes,
            "tone": tone,
            "length": length,
            "original_email": original_email,
        }
    )
    return final_state["result"]
