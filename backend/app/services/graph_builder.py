from backend.app.utils.mapper import load_all_data

def build_graph():
    data = load_all_data()

    nodes = []
    links = []

    added_nodes = set()

    # ---------------------------
    # HELPER FUNCTION
    # ---------------------------
    def add_node(node_id, node_type, extra={}):
        if node_id not in added_nodes:
            nodes.append({
                "id": node_id,
                "type": node_type,
                "data": extra
            })
            added_nodes.add(node_id)

    def add_edge(source, target, relation):
        links.append({
            "source": source,
            "target": target,
            "label": relation
        })

    # ---------------------------
    # 1. CUSTOMERS → ORDERS
    # ---------------------------
    orders = data["orders"]

    for _, row in orders.iterrows():
        cust_id = f"CUST_{row.get('SoldToParty', 'UNK')}"
        order_id = f"ORD_{row.get('SalesOrder', 'UNK')}"

        add_node(cust_id, "customer")
        add_node(order_id, "order", row.to_dict())

        add_edge(cust_id, order_id, "PLACED")

    # ---------------------------
    # 2. ORDER → ITEMS → PRODUCT
    # ---------------------------
    items = data["order_items"]

    for _, row in items.iterrows():
        order_id = f"ORD_{row.get('SalesOrder', 'UNK')}"
        item_id = f"ITEM_{row.get('SalesOrder')}_{row.get('SalesOrderItem')}"
        product_id = f"PROD_{row.get('Material', 'UNK')}"

        add_node(item_id, "order_item")
        add_node(product_id, "product")

        add_edge(order_id, item_id, "HAS_ITEM")
        add_edge(item_id, product_id, "CONTAINS_PRODUCT")

    # ---------------------------
    # 3. ORDER → DELIVERY
    # ---------------------------
    delivery = data["delivery"]

    for _, row in delivery.iterrows():
        order_id = f"ORD_{row.get('ReferenceSDDocument', 'UNK')}"
        delivery_id = f"DEL_{row.get('DeliveryDocument', 'UNK')}"

        add_node(delivery_id, "delivery", row.to_dict())

        add_edge(order_id, delivery_id, "DELIVERED_AS")

    # ---------------------------
    # 4. DELIVERY → INVOICE
    # ---------------------------
    invoices = data["invoices"]

    for _, row in invoices.iterrows():
        delivery_id = f"DEL_{row.get('ReferenceSDDocument', 'UNK')}"
        invoice_id = f"INV_{row.get('BillingDocument', 'UNK')}"

        add_node(invoice_id, "invoice", row.to_dict())

        add_edge(delivery_id, invoice_id, "BILLED_AS")

    # ---------------------------
    # 5. INVOICE → PAYMENT
    # ---------------------------
    payments = data["finance_payment"]

    for _, row in payments.iterrows():
        invoice_id = f"INV_{row.get('AccountingDocument', 'UNK')}"
        payment_id = f"PAY_{row.get('AccountingDocument', 'UNK')}"

        add_node(payment_id, "payment", row.to_dict())

        add_edge(invoice_id, payment_id, "PAID_BY")

    print(f"Graph built: {len(nodes)} nodes, {len(links)} edges")

    return {
        "nodes": nodes,
        "links": links
    }