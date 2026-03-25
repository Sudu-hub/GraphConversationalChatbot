from backend.app.services.llm_service import parse_query
import json

import re

# 🔥 GUARDRAILS
def is_valid_query(question):
    allowed = [
        "order", "invoice", "billing",
        "delivery", "journal", "payment",
        "customer", "product", "flow"
    ]
    return any(word in question.lower() for word in allowed)


# 🔥 INTENT DETECTION
def detect_intent(question):
    q = question.lower()

    if "trace" in q or "flow" in q:
        return "TRACE_FLOW"

    if "journal" in q:
        return "JOURNAL_LOOKUP"

    if "broken" in q or "missing" in q:
        return "BROKEN_FLOW"

    return "GENERIC"


# 🔥 TRACE FLOW (BFS)
def trace_flow(target_id, graph):
    nodes = graph["nodes"]
    links = graph["links"]

    visited = set()
    queue = [target_id]

    result_nodes = set()
    result_links = []

    while queue:
        current = queue.pop(0)

        for link in links:
            source = str(link["source"])
            target = str(link["target"])

            if current in source or current in target:
                result_links.append(link)

                if source not in visited:
                    visited.add(source)
                    queue.append(source)
                    result_nodes.add(source)

                if target not in visited:
                    visited.add(target)
                    queue.append(target)
                    result_nodes.add(target)

    return list(result_nodes), result_links


# 🔥 JOURNAL LOOKUP
def find_journal_entry(target_id, graph):
    for link in graph["links"]:
        source = str(link["source"])
        target = str(link["target"])

        if target_id in source and "JRN" in target:
            return target

    return None


# 🔥 BROKEN FLOW
def find_broken_flows(graph):
    sources = set(str(l["source"]) for l in graph["links"])
    nodes = graph["nodes"]

    broken = []

    for node in nodes:
        node_id = str(node["id"])
        if node_id not in sources:
            broken.append(node_id)

    return broken[:20]


# 🔥 MAIN FUNCTION
def process_query(question, graph):
    # 🚫 Guardrails
    if not is_valid_query(question):
        return {
            "answer": "This system is designed to answer questions related to the dataset only.",
            "ids": [],
            "links": []
        }

    intent = detect_intent(question)
    ids = re.findall(r"\d+", question)
    target_id = ids[0] if ids else None

    # 🔥 TRACE FLOW
    if intent == "TRACE_FLOW" and target_id:
        nodes, links = trace_flow(target_id, graph)

        return {
            "answer": f"Showing full lifecycle for {target_id}",
            "ids": nodes,
            "links": links
        }

    # 🔥 JOURNAL
    if intent == "JOURNAL_LOOKUP" and target_id:
        journal = find_journal_entry(target_id, graph)

        if journal:
            return {
                "answer": f"Journal entry linked to {target_id} is {journal}",
                "ids": [journal],
                "links": []
            }

    # 🔥 BROKEN
    if intent == "BROKEN_FLOW":
        broken = find_broken_flows(graph)

        return {
            "answer": f"Found {len(broken)} broken/incomplete flows",
            "ids": broken,
            "links": []
        }

    return {
        "answer": "Couldn't understand query",
        "ids": [],
        "links": []
    }