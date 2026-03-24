from backend.app.utils.loader import load_folder

orders = load_folder("sales_order_headers")

print("Total orders:", len(orders))
print("Sample:", orders[0])