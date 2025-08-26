import csv
from datetime import datetime

# Utility for logging
def log(message):
    with open("log.txt", "a") as f:
        f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] {message}\n")

class Order:
    discount_rate = 0  # global discount %

    # Decorator for automatic logging
    @staticmethod
    def log_action(func):
        def wrapper(self, *args, **kwargs):
            log(f"Executed {func.__name__}")
            return func(self, *args, **kwargs)
        return wrapper

    def __init__(self):
        self.items = []  # list of (name, price, qty)

    @log_action
    def add_item_by_id(self, product_id, quantity):
        if not Order.is_valid_product_id(product_id):
            log(f"Invalid product ID attempt: {product_id}")
            return
        with open("products.csv", newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row["id"] == str(product_id):
                    name, price = row["name"], float(row["price"])
                    self.items.append((name, price, quantity))
                    log(f"Added item: {name} (x{quantity}) - Total: {price * quantity}")
                    break

    @log_action
    def calculate_total(self):
        total = sum(price * qty for _, price, qty in self.items)
        if Order.discount_rate > 0:
            total *= (1 - Order.discount_rate / 100)
        log(f"Calculated total with discount: {total}")
        return total

    @classmethod
    @log_action
    def set_discount(cls, discount_rate):
        cls.discount_rate = discount_rate
        log(f"Discount set to {discount_rate}%")

    @staticmethod
    def is_valid_product_id(product_id):
        with open("products.csv", newline="") as f:
            reader = csv.DictReader(f)
            return any(row["id"] == str(product_id) for row in reader)

# ------------------ Testing ------------------
if __name__ == "__main__":
    order = Order()
    order.add_item_by_id(1, 2)   # Laptop x2
    order.add_item_by_id(2, 1)   # Phone x1
    order.add_item_by_id(99, 3)  # Invalid ID
    Order.set_discount(10)       # 10% discount
    total = order.calculate_total()
    print("Final Total:", total)
