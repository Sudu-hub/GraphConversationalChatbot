import re

def is_valid_query(question):
    allowed = [
        "order", "invoice", "billing",
        "delivery", "journal", "payment",
        "customer", "product", "flow"
    ]
    return any(word in question.lower() for word in allowed)


def detect_intent(question):
    q = question.lower()

    if "trace" in q or "flow" in q:
        return "TRACE_FLOW"

    if "journal" in q:
        return "JOURNAL_LOOKUP"

    if "broken" in q:
        return "BROKEN_FLOW"

    return "GENERIC"


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


def process_query(question, graph):
    if not is_valid_query(question):
        return {
            "answer": "This system is designed to answer dataset-related questions only.",
            "ids": [],
            "links": []
        }

    intent = detect_intent(question)

    ids = re.findall(r"\d+", question)
    target_id = ids[0] if ids else None

    if intent == "TRACE_FLOW" and target_id:
        nodes, links = trace_flow(target_id, graph)

        return {
            "answer": f"Showing lifecycle for {target_id}",
            "ids": nodes,
            "links": links
        }

    return {
        "answer": "Couldn't understand query",
        "ids": [],
        "links": []
    }