from backend.app.utils.loader import load_folder

datasets = {
    "orders": load_folder("sales_order_headers"),
    "order_item": load_folder("sales_order_items"),
    "order_schedule": load_folder("sales_order_schedule_lines"),
    "invoices": load_folder("billing_document_headers"),
    "invoices_cancellations": load_folder("billing_document_cancellations"),
    "invoices_items": load_folder("billing_document_items"),
    "finance_journal": load_folder("journal_entry_items_accounts_receivable"),
    "finance_payment": load_folder("payments_accounts_receivable"),
    "customers": load_folder("business_partners"),
    "customers_address": load_folder("business_partner_addresses"),
    "customers_company": load_folder("customer_company_assignments"),
    "customers_sales": load_folder("customer_sales_area_assignments"),
    "delivery": load_folder("outbound_delivery_headers"),
    "delivery_items": load_folder("outbound_delivery_items"),
    "products": load_folder("products"),
    "product_descriptions": load_folder("product_descriptions"),
    "product_plants": load_folder("product_plants"),
    "product_storage_locations": load_folder("product_storage_locations"),
    "plants": load_folder("plants"),
}


import os

output_folder = "csv_output"
os.makedirs(output_folder, exist_ok=True)

for name, df in datasets.items():
    df.to_csv(os.path.join(output_folder, f"{name}.csv"), index=False)