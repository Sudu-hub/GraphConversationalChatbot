import networkx as nx

from backend.app.utils.loader import load_folder


def build_graph():
    G = nx.DiGraph()

    # Load data
    orders = load_folder("sales_order_headers")
    invoices = load_folder("billing_document_headers")
    journal = load_folder("journal_entry_items_accounts_receivable")
    customers = load_folder("business_partners")
    delivery_items = load_folder("outbound_delivery_items")
    billing_items = load_folder("billing_document_items")

    print("Loaded:")
    print("Orders:", len(orders))
    print("Invoices:", len(invoices))
    print("Journal:", len(journal))
    print("Customers:", len(customers))
    print("delivery_items:", len(delivery_items))
    print("billing_items:", len(billing_items))

    # ------------------------
    # 1. Customer → Order
    # ------------------------
    for o in orders:
        order_id = o.get("salesOrder")
        customer_id = o.get("soldToParty")

        if order_id:
            G.add_node(order_id, type="Order")

        if customer_id:
            G.add_node(customer_id, type="Customer")

        if order_id and customer_id:
            G.add_edge(customer_id, order_id, label="PLACED")

    # ------------------------
    # 2. Invoice → JournalEntry
    # ------------------------
    for inv in invoices:
        invoice_id = inv.get("billingDocument")
        journal_id = inv.get("accountingDocument")

        if invoice_id:
            G.add_node(invoice_id, type="Invoice")

        if journal_id:
            G.add_node(journal_id, type="JournalEntry")

        if invoice_id and journal_id:
            G.add_edge(invoice_id, journal_id, label="RECORDED_AS")
        
    for d in delivery_items:
        delivery_id = d.get("deliveryDocument")
        order_id = d.get("referenceSdDocument")

        if delivery_id:
            G.add_node(delivery_id, type="Delivery")

        if order_id:
            G.add_node(order_id, type="Order")

        if delivery_id and order_id:
            G.add_edge(order_id, delivery_id, label="DELIVERED_AS")
        
    for b in billing_items:
        invoice_id = b.get("billingDocument")
        delivery_id = b.get("referenceSdDocument")

        if invoice_id:
            G.add_node(invoice_id, type="Invoice")

        if delivery_id:
            G.add_node(delivery_id, type="Delivery")

        if invoice_id and delivery_id:
            G.add_edge(delivery_id, invoice_id, label="BILLED_AS")
            
    return G