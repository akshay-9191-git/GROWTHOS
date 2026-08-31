from datetime import datetime, timedelta
import random

from app.database import SessionLocal
from app.models.user import User
from app.models.product import Product
from app.models.event import BrowsingEvent
from app.models.cart import CartItem
from app.models.order import Order
from app.models.order_item import OrderItem


random.seed(42)

db = SessionLocal()


# ============================================================
# PRODUCTS
# ============================================================

products_data = [
    {
        "name": "Wireless Headphones",
        "category": "Audio",
        "description": "Premium wireless headphones with noise cancellation",
        "price": 4999,
        "stock": 35,
        "rating": 4.6,
        "image_url": "https://images.example.com/headphones.jpg",
    },
    {
        "name": "Smart Watch Pro",
        "category": "Wearables",
        "description": "Fitness tracking smartwatch with AMOLED display",
        "price": 7999,
        "stock": 20,
        "rating": 4.5,
        "image_url": "https://images.example.com/smartwatch.jpg",
    },
    {
        "name": "Mechanical Keyboard",
        "category": "Computer Accessories",
        "description": "RGB mechanical keyboard for gaming and productivity",
        "price": 3499,
        "stock": 45,
        "rating": 4.7,
        "image_url": "https://images.example.com/keyboard.jpg",
    },
    {
        "name": "Wireless Mouse",
        "category": "Computer Accessories",
        "description": "Ergonomic wireless mouse with precision tracking",
        "price": 1499,
        "stock": 60,
        "rating": 4.4,
        "image_url": "https://images.example.com/mouse.jpg",
    },
    {
        "name": "Laptop Stand",
        "category": "Computer Accessories",
        "description": "Adjustable aluminum laptop stand",
        "price": 1999,
        "stock": 30,
        "rating": 4.5,
        "image_url": "https://images.example.com/laptop-stand.jpg",
    },
    {
        "name": "Running Shoes",
        "category": "Footwear",
        "description": "Lightweight running shoes for everyday training",
        "price": 5999,
        "stock": 25,
        "rating": 4.6,
        "image_url": "https://images.example.com/running-shoes.jpg",
    },
    {
        "name": "Travel Backpack",
        "category": "Bags",
        "description": "Water-resistant backpack with laptop compartment",
        "price": 2999,
        "stock": 40,
        "rating": 4.3,
        "image_url": "https://images.example.com/backpack.jpg",
    },
    {
        "name": "Bluetooth Speaker",
        "category": "Audio",
        "description": "Portable Bluetooth speaker with deep bass",
        "price": 2499,
        "stock": 50,
        "rating": 4.4,
        "image_url": "https://images.example.com/speaker.jpg",
    },
    {
        "name": "Gaming Monitor",
        "category": "Gaming",
        "description": "27-inch 165Hz gaming monitor",
        "price": 18999,
        "stock": 12,
        "rating": 4.8,
        "image_url": "https://images.example.com/monitor.jpg",
    },
    {
        "name": "Gaming Mouse",
        "category": "Gaming",
        "description": "High precision gaming mouse with programmable buttons",
        "price": 2499,
        "stock": 35,
        "rating": 4.5,
        "image_url": "https://images.example.com/gaming-mouse.jpg",
    },
    {
        "name": "USB-C Hub",
        "category": "Computer Accessories",
        "description": "Multi-port USB-C hub for laptops",
        "price": 1799,
        "stock": 55,
        "rating": 4.2,
        "image_url": "https://images.example.com/usb-hub.jpg",
    },
    {
        "name": "Power Bank",
        "category": "Electronics",
        "description": "20000mAh fast charging power bank",
        "price": 2199,
        "stock": 70,
        "rating": 4.4,
        "image_url": "https://images.example.com/powerbank.jpg",
    },
    {
        "name": "Smartphone Tripod",
        "category": "Photography",
        "description": "Adjustable tripod for smartphones and cameras",
        "price": 1299,
        "stock": 45,
        "rating": 4.1,
        "image_url": "https://images.example.com/tripod.jpg",
    },
    {
        "name": "Webcam Full HD",
        "category": "Computer Accessories",
        "description": "1080p webcam for meetings and streaming",
        "price": 2999,
        "stock": 25,
        "rating": 4.3,
        "image_url": "https://images.example.com/webcam.jpg",
    },
    {
        "name": "Desk Lamp",
        "category": "Home Office",
        "description": "LED desk lamp with adjustable brightness",
        "price": 999,
        "stock": 80,
        "rating": 4.2,
        "image_url": "https://images.example.com/lamp.jpg",
    },
    {
        "name": "Fitness Band",
        "category": "Wearables",
        "description": "Affordable fitness and activity tracker",
        "price": 1999,
        "stock": 45,
        "rating": 4.3,
        "image_url": "https://images.example.com/fitness-band.jpg",
    },
    {
        "name": "Coffee Maker",
        "category": "Home",
        "description": "Compact automatic coffee maker",
        "price": 4499,
        "stock": 18,
        "rating": 4.5,
        "image_url": "https://images.example.com/coffee-maker.jpg",
    },
    {
        "name": "Air Purifier",
        "category": "Home",
        "description": "Compact HEPA air purifier",
        "price": 8999,
        "stock": 15,
        "rating": 4.6,
        "image_url": "https://images.example.com/air-purifier.jpg",
    },
    {
        "name": "Portable SSD",
        "category": "Storage",
        "description": "1TB high-speed portable SSD",
        "price": 6999,
        "stock": 22,
        "rating": 4.7,
        "image_url": "https://images.example.com/ssd.jpg",
    },
    {
        "name": "Phone Fast Charger",
        "category": "Electronics",
        "description": "65W USB-C fast charger",
        "price": 1599,
        "stock": 65,
        "rating": 4.5,
        "image_url": "https://images.example.com/charger.jpg",
    },
]


# ============================================================
# USERS
# ============================================================

print("Creating users...")

users = []

for i in range(1, 51):
    user = User(
        name=f"Customer {i}",
        email=f"customer{i}@growthos.demo",
        created_at=datetime.utcnow() - timedelta(days=random.randint(1, 180)),
    )

    db.add(user)
    users.append(user)

db.commit()

print(f"Created {len(users)} users.")


# ============================================================
# PRODUCTS
# ============================================================

print("Creating products...")

products = []

for data in products_data:
    product = Product(**data)

    db.add(product)
    products.append(product)

db.commit()

print(f"Created {len(products)} products.")


# ============================================================
# BROWSING EVENTS
# ============================================================

print("Creating browsing events...")

event_types = [
    "view",
    "search",
    "add_to_cart",
]

events = []

for user in users:

    # Normal browsing behavior
    for _ in range(random.randint(3, 8)):

        product = random.choice(products)

        event = BrowsingEvent(
            user_id=user.id,
            product_id=product.id,
            event_type=random.choice(event_types),
            created_at=datetime.utcnow()
            - timedelta(
                days=random.randint(0, 30),
                hours=random.randint(0, 23),
            ),
        )

        db.add(event)
        events.append(event)


# ============================================================
# HIGH-INTENT CUSTOMER PATTERN
# ============================================================

# Customer 1 repeatedly views Wireless Headphones
# but does not purchase them.

high_intent_user = users[0]
high_intent_product = products[0]

for i in range(8):

    event = BrowsingEvent(
        user_id=high_intent_user.id,
        product_id=high_intent_product.id,
        event_type="view",
        created_at=datetime.utcnow() - timedelta(hours=8 - i),
    )

    db.add(event)
    events.append(event)


# Add the product to their cart
cart = CartItem(
    user_id=high_intent_user.id,
    product_id=high_intent_product.id,
    quantity=1,
    created_at=datetime.utcnow() - timedelta(hours=2),
)

db.add(cart)


# ============================================================
# SECOND HIGH-INTENT CUSTOMER
# ============================================================

second_user = users[1]
second_product = products[8]  # Gaming Monitor

for i in range(6):

    event = BrowsingEvent(
        user_id=second_user.id,
        product_id=second_product.id,
        event_type="view",
        created_at=datetime.utcnow() - timedelta(hours=10 - i),
    )

    db.add(event)
    events.append(event)


cart = CartItem(
    user_id=second_user.id,
    product_id=second_product.id,
    quantity=1,
    created_at=datetime.utcnow() - timedelta(hours=1),
)

db.add(cart)


db.commit()

print(f"Created {len(events)} browsing events.")


# ============================================================
# RANDOM CARTS
# ============================================================

print("Creating additional abandoned carts...")

for user in users[2:15]:

    product = random.choice(products)

    cart = CartItem(
        user_id=user.id,
        product_id=product.id,
        quantity=random.randint(1, 2),
        created_at=datetime.utcnow() - timedelta(
            days=random.randint(0, 7)
        ),
    )

    db.add(cart)

db.commit()


# ============================================================
# ORDERS
# ============================================================

print("Creating orders...")

orders = []

for user in users[10:35]:

    product = random.choice(products)

    quantity = random.randint(1, 3)

    total = product.price * quantity

    order = Order(
        user_id=user.id,
        total_amount=total,
        status="completed",
        created_at=datetime.utcnow()
        - timedelta(days=random.randint(1, 60)),
    )

    db.add(order)
    db.flush()

    order_item = OrderItem(
        order_id=order.id,
        product_id=product.id,
        quantity=quantity,
        price=product.price,
    )

    db.add(order_item)

    orders.append(order)


db.commit()

print(f"Created {len(orders)} orders.")


# ============================================================
# FINISH
# ============================================================

db.close()

print()
print("========================================")
print("GrowthOS seed completed successfully!")
print("========================================")
print(f"Users:           {len(users)}")
print(f"Products:        {len(products)}")
print(f"Browsing events: {len(events)}")
print(f"Orders:          {len(orders)}")
print("========================================")