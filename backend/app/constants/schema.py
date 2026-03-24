NODE_TYPES = [
    "Customer", "Order", "OrderItem",
    "Delivery", "Invoice", "JournalEntry",
    "Payment", "Product", "Address"
]

RELATIONSHIPS = [
    ("Customer", "PLACED", "Order"),
    ("Order", "HAS_ITEM", "OrderItem"),
    ("OrderItem", "REFERENCES", "Product"),
    ("Order", "DELIVERED_AS", "Delivery"),
    ("Delivery", "BILLED_AS", "Invoice"),
    ("Invoice", "RECORDED_AS", "JournalEntry"),
    ("JournalEntry", "CLEARED_BY", "Payment"),
    ("Customer", "HAS_ADDRESS", "Address")
]