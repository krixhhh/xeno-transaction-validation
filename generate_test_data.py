import pandas as pd
import random
from datetime import datetime, timedelta

def generate_large_dataset(filename="large_test_transactions.csv", num_rows=1200):
    print(f"Generating {num_rows} transaction records in {filename}...")
    
    categories = {
        "Electronics": ["Smartphone", "Laptop", "Bluetooth Earbuds", "Smart Watch", "Power Bank"],
        "Computer Accessories": ["Mechanical Keyboard", "Wireless Mouse", "USB-C Hub", "Monitor Arm"],
        "Home Appliances": ["Air Fryer", "Robot Vacuum", "Humidifier", "Electric Kettle"],
        "Apparel": ["Performance Tee", "Hoodie", "Running Shoes", "Athletic Shorts"],
        "Office Supplies": ["Ergonomic Chair", "Desk Mat", "Notebook Pack", "LED Desk Lamp"]
    }
    
    payment_modes = ["Credit Card", "Debit Card", "UPI", "PayPal", "Wallet", "Net Banking"]
    payment_statuses = ["Success", "Success", "Success", "Failed", "Pending"] # heavily weigh success
    
    countries = ["India", "Singapore", "United States", "Malaysia"]
    
    rows = []
    
    # Generate some duplicate IDs to test duplicate checking
    seen_ids = set()
    
    start_date = datetime(2026, 1, 1)
    
    for i in range(num_rows):
        # Generate Order ID
        # 1% chance of duplicate ID
        if i > 50 and random.random() < 0.01:
            order_id = f"TXN-{random.randint(1000, 1050)}"
        else:
            order_id = f"TXN-{1000 + i}"
            
        # 0.5% chance of missing order_id
        if random.random() < 0.005:
            order_id = ""
            
        # Date: DD-MM-YYYY [HH:MM:SS]
        # 1% chance of invalid date format
        dt = start_date + timedelta(days=random.randint(0, 150), hours=random.randint(0, 23), minutes=random.randint(0, 59))
        if random.random() < 0.01:
            tx_date = "2026/15/06" # Bad date
        elif random.random() < 0.005:
            tx_date = "" # Missing
        else:
            tx_date = dt.strftime("%d-%m-%Y %H:%M:%S")
            
        cust_id = f"CUST-{random.randint(10000, 99999)}"
        
        category = random.choice(list(categories.keys()))
        product = random.choice(categories[category])
        
        # Quantity
        # 1% chance of invalid quantity (0, negative, or text)
        qty_rand = random.random()
        if qty_rand < 0.005:
            qty = "0"
        elif qty_rand < 0.01:
            qty = "-3"
        elif qty_rand < 0.015:
            qty = "string_qty"
        else:
            qty = str(random.randint(1, 5))
            
        # Amount
        # 1% chance of negative amount or invalid numeric
        amt_rand = random.random()
        if amt_rand < 0.005:
            amount = "-45.00"
        elif amt_rand < 0.01:
            amount = "invalid_price"
        else:
            amount = f"{random.uniform(10.0, 500.0):.2f}"
            
        # Payment details
        pay_mode = random.choice(payment_modes)
        # 0.5% chance of invalid payment mode
        if random.random() < 0.005:
            pay_mode = "Bitcoin"
            
        pay_status = random.choice(payment_statuses)
        
        # Customer country and phone
        country = random.choice(countries)
        
        # Phone numbers:
        # India = 10 digits
        # Singapore = 8 digits
        # US = 10 digits
        # Malaysia = 9-10 digits
        # Generate phone based on country, with a 2% error rate (wrong length)
        phone_error = random.random() < 0.02
        
        if country == "India":
            phone = "".join([str(random.randint(0, 9)) for _ in range(9 if phone_error else 10)])
        elif country == "Singapore":
            phone = "".join([str(random.randint(0, 9)) for _ in range(6 if phone_error else 8)])
        elif country == "United States":
            phone = "".join([str(random.randint(0, 9)) for _ in range(12 if phone_error else 10)])
        else: # Malaysia
            phone = "".join([str(random.randint(0, 9)) for _ in range(7 if phone_error else 9)])
            
        # 0.5% chance of missing phone number
        if random.random() < 0.005:
            phone = ""
            
        rows.append({
            "order_id": order_id,
            "transaction_date": tx_date,
            "customer_id": cust_id,
            "product_name": product,
            "product_category": category,
            "quantity": qty,
            "amount": amount,
            "payment_mode": pay_mode,
            "payment_status": pay_status,
            "country": country,
            "phone_number": phone
        })
        
    df = pd.DataFrame(rows)
    df.to_csv(filename, index=False)
    print(f"Successfully wrote {num_rows} records to {filename}.")
    print("This file contains standard transaction values, plus a small percentage of errors:")
    print(" - Duplicate order IDs")
    print(" - Negative/alphanumeric amounts & quantities")
    print(" - Invalid country-specific phone lengths (e.g. India != 10, Singapore != 8 digits)")
    print(" - Invalid date/time formatting patterns")

if __name__ == "__main__":
    generate_large_dataset()
