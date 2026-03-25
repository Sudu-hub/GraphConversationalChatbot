from backend.app.utils.loader import load_folder

def load_all_data():
    data = {}

    data["orders"] = load_folder("sales_order_headers")
    data["order_items"] = load_folder("sales_order_items")
    data["order_schedule"] = load_folder("sales_order_schedule_lines")

    data["invoices"] = load_folder("billing_document_headers")
    data["invoice_items"] = load_folder("billing_document_items")
    data["invoice_cancellations"] = load_folder("billing_document_cancellations")

    data["finance_journal"] = load_folder("journal_entry_items_accounts_receivable")
    data["finance_payment"] = load_folder("payments_accounts_receivable")

    data["customers"] = load_folder("business_partners")
    data["customer_address"] = load_folder("business_partner_addresses")
    data["customer_company"] = load_folder("customer_company_assignments")
    data["customer_sales"] = load_folder("customer_sales_area_assignments")

    data["delivery"] = load_folder("outbound_delivery_headers")
    data["delivery_items"] = load_folder("outbound_delivery_items")

    data["products"] = load_folder("products")
    data["product_descriptions"] = load_folder("product_descriptions")
    data["product_plants"] = load_folder("product_plants")
    data["product_storage"] = load_folder("product_storage_locations")

    data["plants"] = load_folder("plants")

    return data