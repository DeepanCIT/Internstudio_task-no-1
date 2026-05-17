"""
Seed the database with realistic product catalog and synthetic user interactions.
Run: python data/seed_data.py  (from the backend/ directory)
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
from werkzeug.security import generate_password_hash
from app import create_app
from database import db, User, Product, BrowsingHistory, Purchase, Rating

PRODUCTS = [
    # Electronics
    {"name":"Sony WH-1000XM5 Headphones","description":"Industry-leading noise cancelling wireless headphones with 30hr battery and multipoint connection","category":"Electronics","subcategory":"Audio","price":349.99,"brand":"Sony","tags":"headphones,wireless,noise-cancelling,bluetooth,audio,music","image_url":"https://source.unsplash.com/400x400/?headphones"},
    {"name":"Apple iPad Air 5th Gen","description":"10.9-inch Liquid Retina display with M1 chip, 5G support and Touch ID for the ultimate iPad experience","category":"Electronics","subcategory":"Tablets","price":749.00,"brand":"Apple","tags":"tablet,apple,ipad,m1,5g,touch-id,retina","image_url":"https://source.unsplash.com/400x400/?ipad,tablet"},
    {"name":"Samsung 4K QLED Smart TV 55\"","description":"Quantum Dot technology delivers brilliant colour. Smart TV with voice assistants and gaming mode","category":"Electronics","subcategory":"TVs","price":899.99,"brand":"Samsung","tags":"tv,smart-tv,4k,qled,samsung,gaming,hdr","image_url":"https://source.unsplash.com/400x400/?smart-tv"},
    {"name":"Logitech MX Master 3S Mouse","description":"Advanced wireless mouse with 8K DPI, quiet clicks, and ergonomic design for productivity","category":"Electronics","subcategory":"Peripherals","price":99.99,"brand":"Logitech","tags":"mouse,wireless,ergonomic,productivity,logitech,bluetooth","image_url":"https://source.unsplash.com/400x400/?computer-mouse"},
    {"name":"Dell XPS 15 Laptop","description":"15.6-inch OLED display, Intel Core i7, 32GB RAM, 1TB SSD — built for creators","category":"Electronics","subcategory":"Laptops","price":1899.00,"brand":"Dell","tags":"laptop,dell,xps,oled,i7,creator,portable","image_url":"https://source.unsplash.com/400x400/?laptop"},
    {"name":"Anker PowerCore 26800 mAh","description":"High-capacity portable charger with 3 USB-A ports and 18W fast charging","category":"Electronics","subcategory":"Accessories","price":45.99,"brand":"Anker","tags":"powerbank,charger,anker,portable,fast-charge,travel","image_url":"https://source.unsplash.com/400x400/?powerbank"},
    {"name":"Canon EOS R50 Mirrorless Camera","description":"24.2MP APS-C sensor, 4K video, fast AF tracking — perfect for vloggers and enthusiasts","category":"Electronics","subcategory":"Cameras","price":679.00,"brand":"Canon","tags":"camera,mirrorless,canon,4k,photography,vlogging","image_url":"https://source.unsplash.com/400x400/?mirrorless-camera"},
    {"name":"Bose QuietComfort Earbuds II","description":"True wireless earbuds with personalised noise cancellation and up to 6-hr battery","category":"Electronics","subcategory":"Audio","price":279.99,"brand":"Bose","tags":"earbuds,wireless,bose,noise-cancelling,bluetooth,audio","image_url":"https://source.unsplash.com/400x400/?earbuds"},
    # Fashion
    {"name":"Levi's 511 Slim Jeans","description":"Classic slim-fit jeans in stretch denim for all-day comfort. Available in multiple washes","category":"Fashion","subcategory":"Men's Clothing","price":69.99,"brand":"Levi's","tags":"jeans,denim,slim-fit,casual,men,levis","image_url":"https://source.unsplash.com/400x400/?jeans"},
    {"name":"Nike Air Force 1 '07","description":"The radiance lives on in the Nike Air Force 1 '07, the basketball original that puts a fresh spin on a classic design","category":"Fashion","subcategory":"Footwear","price":110.00,"brand":"Nike","tags":"shoes,sneakers,nike,air-force,classic,white,casual","image_url":"https://source.unsplash.com/400x400/?sneakers"},
    {"name":"Adidas Ultraboost 23","description":"Maximum energy return with Boost midsole and Primeknit+ upper. Premium running shoe","category":"Fashion","subcategory":"Footwear","price":190.00,"brand":"Adidas","tags":"running,shoes,adidas,ultraboost,boost,sport,performance","image_url":"https://source.unsplash.com/400x400/?running-shoes"},
    {"name":"Zara Oversized Blazer","description":"Structured oversized blazer in a wool blend. Notch lapels and a relaxed silhouette","category":"Fashion","subcategory":"Women's Clothing","price":89.99,"brand":"Zara","tags":"blazer,women,oversized,formal,smart-casual,zara","image_url":"https://source.unsplash.com/400x400/?blazer"},
    {"name":"Ray-Ban Aviator Classic","description":"Iconic teardrop lenses in gunmetal with G-15 glass lens. UV400 protection","category":"Fashion","subcategory":"Accessories","price":163.00,"brand":"Ray-Ban","tags":"sunglasses,aviator,ray-ban,uv-protection,classic,style","image_url":"https://source.unsplash.com/400x400/?sunglasses"},
    # Home & Kitchen
    {"name":"Instant Pot Duo 7-in-1","description":"7-in-1 multi-use programmable pressure cooker: pressure cooker, slow cooker, rice cooker and more","category":"Home & Kitchen","subcategory":"Appliances","price":89.99,"brand":"Instant Pot","tags":"pressure-cooker,kitchen,instant-pot,multi-cooker,cooking,appliance","image_url":"https://source.unsplash.com/400x400/?pressure-cooker"},
    {"name":"Ninja Air Fryer Max XL","description":"5.5 qt air fryer with Max Crisp Technology and 6 cooking functions. Dishwasher-safe parts","category":"Home & Kitchen","subcategory":"Appliances","price":119.99,"brand":"Ninja","tags":"air-fryer,ninja,kitchen,cooking,healthy,crispy,appliance","image_url":"https://source.unsplash.com/400x400/?air-fryer"},
    {"name":"Dyson V15 Detect Vacuum","description":"The most powerful, intelligent cordless vacuum with laser dust detection and HEPA filtration","category":"Home & Kitchen","subcategory":"Cleaning","price":749.99,"brand":"Dyson","tags":"vacuum,cordless,dyson,cleaning,hepa,powerful,home","image_url":"https://source.unsplash.com/400x400/?vacuum"},
    {"name":"Philips Hue Smart Bulbs 4-Pack","description":"16 million colours, works with Alexa and Google Home. Set scenes and schedules via app","category":"Home & Kitchen","subcategory":"Smart Home","price":59.99,"brand":"Philips","tags":"smart-bulb,philips-hue,smart-home,alexa,colour,lighting,rgb","image_url":"https://source.unsplash.com/400x400/?smart-bulb"},
    {"name":"IKEA ALEX Drawer Unit","description":"Smooth-running drawers for office or bedroom. White powder-coated steel. 6 spacious drawers","category":"Home & Kitchen","subcategory":"Furniture","price":149.00,"brand":"IKEA","tags":"drawer,furniture,ikea,storage,desk,organiser,white","image_url":"https://source.unsplash.com/400x400/?drawer"},
    # Sports & Fitness
    {"name":"Fitbit Charge 6","description":"Advanced health and fitness tracker with GPS, SpO2, ECG app and Google Maps integration","category":"Sports","subcategory":"Wearables","price":159.95,"brand":"Fitbit","tags":"fitness-tracker,fitbit,gps,health,heart-rate,wearable,smartwatch","image_url":"https://source.unsplash.com/400x400/?fitness-tracker"},
    {"name":"Bowflex SelectTech 552 Dumbbells","description":"Adjustable dumbbells replace 15 sets of weights. Select from 5 to 52.5 lb in seconds","category":"Sports","subcategory":"Weights","price":429.00,"brand":"Bowflex","tags":"dumbbells,weights,bowflex,gym,fitness,strength,home-gym","image_url":"https://source.unsplash.com/400x400/?dumbbell"},
    {"name":"Manduka PRO Yoga Mat","description":"6mm thick, lifetime guarantee. Non-slip grip and dense cushioning for joint protection","category":"Sports","subcategory":"Yoga","price":120.00,"brand":"Manduka","tags":"yoga-mat,manduka,yoga,fitness,non-slip,exercise,meditation","image_url":"https://source.unsplash.com/400x400/?yoga-mat"},
    {"name":"Garmin Forerunner 255","description":"Running GPS smartwatch with training readiness, daily suggested workouts and up to 14-day battery","category":"Sports","subcategory":"Wearables","price":349.99,"brand":"Garmin","tags":"smartwatch,garmin,gps,running,sport,battery,fitness","image_url":"https://source.unsplash.com/400x400/?gps-watch"},
    # Books
    {"name":"Atomic Habits by James Clear","description":"Tiny changes, remarkable results. The proven framework for building good habits and breaking bad ones","category":"Books","subcategory":"Self-Help","price":18.99,"brand":"Avery","tags":"habit,self-help,productivity,psychology,bestseller,non-fiction","image_url":"https://source.unsplash.com/400x400/?book"},
    {"name":"The Psychology of Money","description":"Timeless lessons on wealth, greed, and happiness. Morgan Housel's bestselling personal finance guide","category":"Books","subcategory":"Finance","price":16.99,"brand":"Harriman House","tags":"finance,money,investing,psychology,personal-finance,non-fiction","image_url":"https://source.unsplash.com/400x400/?finance-book"},
    {"name":"Dune by Frank Herbert","description":"The epic science fiction masterpiece. A sweeping tale of politics, religion, ecology and power","category":"Books","subcategory":"Science Fiction","price":14.99,"brand":"Ace","tags":"sci-fi,dune,frank-herbert,epic,fantasy,fiction,classic","image_url":"https://source.unsplash.com/400x400/?science-fiction-book"},
]

LOCAL_IMAGE_PREFIX = "/images/"

DEMO_USERS = [
    {"username":"alice","email":"alice@demo.com","password":"demo1234","age":28,"gender":"Female","location":"New York"},
    {"username":"bob","email":"bob@demo.com","password":"demo1234","age":34,"gender":"Male","location":"London"},
    {"username":"carol","email":"carol@demo.com","password":"demo1234","age":22,"gender":"Female","location":"Mumbai"},
    {"username":"dave","email":"dave@demo.com","password":"demo1234","age":45,"gender":"Male","location":"Toronto"},
    {"username":"eve","email":"eve@demo.com","password":"demo1234","age":31,"gender":"Female","location":"Sydney"},
]

def seed():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        # --- Products ---
        product_objects = []
        for p in PRODUCTS:
            image_url = p.get("image_url")
            if not image_url or not str(image_url).startswith(LOCAL_IMAGE_PREFIX):
                image_url = None

            product_objects.append(Product(
                name=p["name"], description=p["description"],
                category=p["category"], subcategory=p["subcategory"],
                price=p["price"], brand=p["brand"], tags=p["tags"],
                image_url=image_url,
                avg_rating=round(random.uniform(3.5, 5.0), 1),
                reviews_count=random.randint(50, 2000),
                stock=random.randint(10, 500)
            ))
        db.session.add_all(product_objects)
        db.session.commit()
        print(f"✅  Inserted {len(product_objects)} products")

        # --- Demo Users ---
        user_objects = []
        for u in DEMO_USERS:
            user_objects.append(User(
                username=u["username"], email=u["email"],
                password_hash=generate_password_hash(u["password"]),
                age=u["age"], gender=u["gender"], location=u["location"]
            ))
        db.session.add_all(user_objects)
        db.session.commit()
        print(f"✅  Inserted {len(user_objects)} demo users")

        products = Product.query.all()
        users    = User.query.all()

        # --- Synthetic Browsing History ---
        for user in users:
            viewed = random.sample(products, k=random.randint(6, 14))
            for p in viewed:
                db.session.add(BrowsingHistory(
                    user_id=user.id, product_id=p.id,
                    duration=random.randint(15, 300)
                ))

        # --- Synthetic Purchases ---
        for user in users:
            bought = random.sample(products, k=random.randint(2, 6))
            for p in bought:
                db.session.add(Purchase(
                    user_id=user.id, product_id=p.id,
                    quantity=random.randint(1, 3),
                    price_paid=p.price
                ))

        # --- Synthetic Ratings ---
        for user in users:
            rated = random.sample(products, k=random.randint(4, 10))
            for p in rated:
                db.session.add(Rating(
                    user_id=user.id, product_id=p.id,
                    rating=round(random.uniform(2.5, 5.0), 1)
                ))

        db.session.commit()
        print("✅  Inserted synthetic browsing, purchases, and ratings")
        print("\n🎉  Database seeded successfully!")
        print("Demo login → username: alice  password: demo1234")

if __name__ == '__main__':
    seed()
