from backend.app.utils.mapper import load_all_data

def build_graph():
    data = load_all_data()

    nodes = []
    links = []
    added_nodes = set()

    def add_node(node_id, node_type, extra={}):
        if node_id and node_id not in added_nodes:
            nodes.append({
                "id": node_id,
                "type": node_type,
                "data": extra
            })
            added_nodes.add(node_id)

    def add_edge(source, target, relation):
        if source and target:
            links.append({
                "source": source,
                "target": target,
                "label": relation
            })

    # ---------------------------
    # CUSTOMER → ORDER
    # ---------------------------
    orders = data["orders"]

    print("Orders columns:", orders.columns)

    for _, row in orders.iterrows():
        order_id = f"ORD_{row.get('salesOrder')}"
        cust_id = f"CUST_{row.get('soldToParty')}"

        add_node(order_id, "order", row.to_dict())
        add_node(cust_id, "customer")

        add_edge(cust_id, order_id, "PLACED")

    # ---------------------------
    # ORDER → ITEM → PRODUCT
    # ---------------------------
    items = data["order_items"]

    print("Items columns:", items.columns)

    for _, row in items.iterrows():
        order_id = f"ORD_{row.get('salesOrder')}"
        item_id = f"ITEM_{row.get('salesOrder')}_{row.get('salesOrderItem')}"
        product_id = f"PROD_{row.get('material')}"

        add_node(item_id, "order_item")
        add_node(product_id, "product")

        add_edge(order_id, item_id, "HAS_ITEM")
        add_edge(item_id, product_id, "PRODUCT")

    # ---------------------------
    # ORDER → DELIVERY
    # ---------------------------
    delivery = data["delivery"]

    print("Delivery columns:", delivery.columns)

    for _, row in delivery.iterrows():
        delivery_id = f"DEL_{row.get('deliveryDocument')}"
        order_ref = row.get("referenceSDDocument")

        if order_ref:
            order_id = f"ORD_{order_ref}"

            add_node(delivery_id, "delivery", row.to_dict())
            add_edge(order_id, delivery_id, "DELIVERED")

    # ---------------------------
    # DELIVERY → INVOICE
    # ---------------------------
    invoices = data["invoices"]

    print("Invoice columns:", invoices.columns)

    for _, row in invoices.iterrows():
        invoice_id = f"INV_{row.get('billingDocument')}"
        ref_doc = row.get("referenceSDDocument")

        if ref_doc:
            delivery_id = f"DEL_{ref_doc}"

            add_node(invoice_id, "invoice", row.to_dict())
            add_edge(delivery_id, invoice_id, "BILLED")

    # ---------------------------
    # INVOICE → PAYMENT
    # ---------------------------
    payments = data["finance_payment"]

    print("Payments columns:", payments.columns)

    for _, row in payments.iterrows():
        payment_id = f"PAY_{row.get('accountingDocument')}"
        invoice_ref = row.get("accountingDocument")

        if invoice_ref:
            invoice_id = f"INV_{invoice_ref}"

            add_node(payment_id, "payment", row.to_dict())
            add_edge(invoice_id, payment_id, "PAID")

    print("✅ FINAL GRAPH:", len(nodes), "nodes,", len(links), "edges")

    return {
        "nodes": nodes,
        "links": links
    }