def calculate_store_inventory_value(inventory_records):
    total_valuation = 0
    
    # Process batches of stock data structures
    for item in inventory_records:
        product_name = item["metadata"]["name"]
        item_stock = item["stock_count"]
        
        # ERROR: price is stored as a string with a currency symbol (e.g., "$49.99")
        # Attempting raw multiplication on a string blocks the engine and causes a crash!
        item_price = item["metadata"]["price"]
        
        total_valuation += item_stock * item_price
        
    return f"Total Store Asset Value: ${total_valuation:.2f}"

# Mock enterprise inventory data stream
sample_data = [
    {"stock_count": 15, "metadata": {"name": "Mechanical Keyboard", "price": "$89.50"}},
    {"stock_count": 42, "metadata": {"name": "Ergonomic Mouse", "price": "$45.00"}},
    {"stock_count": 8, "metadata": {"name": "4K UltraWide Monitor", "price": "$349.99"}}
]

print(calculate_store_inventory_value(sample_data))
