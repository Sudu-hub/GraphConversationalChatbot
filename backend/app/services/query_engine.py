import duckdb
from backend.app.utils.mapper import load_all_data
from backend.app.services.llm_service import generate_sql

def process_query(question: str):
    data = load_all_data()

    # 🔥 Example: extract order id from question
    import re
    match = re.search(r'\d+', question)

    if not match:
        return {"answer": "Please provide order ID", "ids": [], "links": []}

    order_id = match.group()

    # 🔥 Build simple path manually (customize later)
    path_ids = []
    path_links = []

    # Order node
    order_node = f"ORD_{order_id}"
    path_ids.append(order_id)

    # Example connections (adjust based on your data)
    invoice_node = f"INV_{order_id}"
    payment_node = f"PAY_{order_id}"

    path_ids.extend([order_id, order_id])

    path_links = [
        {"source": order_node, "target": invoice_node},
        {"source": invoice_node, "target": payment_node},
    ]

    return {
        "answer": f"Showing flow for order {order_id}",
        "ids": [order_id],
        "links": path_links   # 🔥 NEW
    }