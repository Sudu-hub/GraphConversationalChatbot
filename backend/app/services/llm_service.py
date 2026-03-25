def generate_sql(question: str):
    q = question.lower()

    if "order" in q:
        return "SELECT salesOrder FROM orders LIMIT 20"

    if "unbilled" in q:
        return """
        SELECT o.salesOrder
        FROM orders o
        LEFT JOIN invoices i
        ON o.salesOrder = i.referenceSDDocument
        WHERE i.billingDocument IS NULL
        """

    if "invoice" in q:
        return "SELECT billingDocument FROM invoices LIMIT 20"

    if "payment" in q:
        return "SELECT accountingDocument FROM finance_payment LIMIT 20"

    return None  # 🔥 IMPORTANT