"""
Updated seed data with real product images from Unsplash (free, no API key needed).
Run from inside the backend/ folder:
    python data/seed_data.py
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import random
from werkzeug.security import generate_password_hash
from app import create_app
from database import db, User, Product, BrowsingHistory, Purchase, Rating

PRODUCTS = [
    # Electronics
    {"name":"Sony WH-1000XM5 Headphones","description":"Industry-leading noise cancelling wireless headphones with 30-hour battery, multipoint connection, and crystal-clear hands-free calling.","category":"Electronics","subcategory":"Audio","price":349.99,"brand":"Sony","tags":"headphones,wireless,noise-cancelling,bluetooth,audio,music","image_url":"https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400&h=400&fit=crop"},
    {"name":"Apple iPad Air 5th Gen","description":"10.9-inch Liquid Retina display with M1 chip, 5G support and Touch ID for the ultimate iPad experience.","category":"Electronics","subcategory":"Tablets","price":749.00,"brand":"Apple","tags":"tablet,apple,ipad,m1,5g,touch-id,retina","image_url":"https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400&h=400&fit=crop"},
    {"name":"Samsung 4K QLED Smart TV 55\"","description":"Quantum Dot technology delivers brilliant colour. Smart TV with Alexa, Google Assistant and gaming mode.","category":"Electronics","subcategory":"TVs","price":899.99,"brand":"Samsung","tags":"tv,smart-tv,4k,qled,samsung,gaming,hdr","image_url":"https://upload.wikimedia.org/wikipedia/commons/e/e2/LG_smart_TV.jpg"},
    {"name":"Logitech MX Master 3S Mouse","description":"Advanced wireless mouse with 8K DPI, MagSpeed scroll wheel and perfectly sculpted ergonomic design.","category":"Electronics","subcategory":"Peripherals","price":99.99,"brand":"Logitech","tags":"mouse,wireless,ergonomic,productivity,logitech,bluetooth","image_url":"https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=400&h=400&fit=crop"},
    {"name":"Dell XPS 15 Laptop","description":"15.6-inch OLED display, Intel Core i7, 32 GB RAM, 1 TB SSD — built for creative professionals.","category":"Electronics","subcategory":"Laptops","price":1899.00,"brand":"Dell","tags":"laptop,dell,xps,oled,i7,creator,portable","image_url":"https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=400&h=400&fit=crop"},
    {"name":"Anker PowerCore 26800 mAh","description":"High-capacity portable charger with three USB-A ports and 18 W fast charging. Recharge phones up to 6x per charge.","category":"Electronics","subcategory":"Accessories","price":45.99,"brand":"Anker","tags":"powerbank,charger,anker,portable,fast-charge,travel","image_url":"https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=400&h=400&fit=crop"},
    {"name":"Canon EOS R50 Mirrorless Camera","description":"24.2 MP APS-C sensor, 4K video, fast AF subject tracking — perfect for vloggers and enthusiast photographers.","category":"Electronics","subcategory":"Cameras","price":679.00,"brand":"Canon","tags":"camera,mirrorless,canon,4k,photography,vlogging","image_url":"https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=400&h=400&fit=crop"},
    {"name":"Bose QuietComfort Earbuds II","description":"True wireless earbuds with CustomTune personalised noise cancellation and up to 6 hours battery per charge.","category":"Electronics","subcategory":"Audio","price":279.99,"brand":"Bose","tags":"earbuds,wireless,bose,noise-cancelling,bluetooth,audio","image_url":"https://images.unsplash.com/photo-1590658268037-6bf12165a8df?w=400&h=400&fit=crop"},
    # Fashion
    {"name":"Levi's 511 Slim Jeans","description":"Classic slim-fit jeans in stretch denim. Sits below waist with a slim leg from hip to ankle.","category":"Fashion","subcategory":"Men's Clothing","price":69.99,"brand":"Levi's","tags":"jeans,denim,slim-fit,casual,men,levis","image_url":"https://images.unsplash.com/photo-1542272604-787c3835535d?w=400&h=400&fit=crop"},
    {"name":"Nike Air Force 1 '07","description":"The radiance lives on in the Nike Air Force 1 '07, the basketball original that puts a fresh spin on a classic design.","category":"Fashion","subcategory":"Footwear","price":110.00,"brand":"Nike","tags":"shoes,sneakers,nike,air-force,classic,white,casual","image_url":"https://images.unsplash.com/photo-1600269452121-4f2416e55c28?w=400&h=400&fit=crop"},
    {"name":"Adidas Ultraboost 23","description":"Maximum energy return with Boost midsole and Primeknit+ upper. The premium daily running shoe.","category":"Fashion","subcategory":"Footwear","price":190.00,"brand":"Adidas","tags":"running,shoes,adidas,ultraboost,boost,sport,performance","image_url":"https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400&h=400&fit=crop"},
    {"name":"Zara Oversized Blazer","description":"Structured oversized blazer in a premium wool blend. Notch lapels and a relaxed silhouette.","category":"Fashion","subcategory":"Women's Clothing","price":89.99,"brand":"Zara","tags":"blazer,women,oversized,formal,smart-casual,zara","image_url":"https://images.unsplash.com/photo-1591369822096-ffd140ec948f?w=400&h=400&fit=crop"},
    {"name":"Ray-Ban Aviator Classic","description":"Iconic teardrop lenses in gunmetal with G-15 glass lens. Timeless style with UV400 protection.","category":"Fashion","subcategory":"Accessories","price":163.00,"brand":"Ray-Ban","tags":"sunglasses,aviator,ray-ban,uv-protection,classic,style","image_url":"https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=400&h=400&fit=crop"},
    # Home & Kitchen
    {"name":"Instant Pot Duo 7-in-1","description":"7-in-1 multi-use programmable pressure cooker, slow cooker, rice cooker, steamer, saute pan, yogurt maker and warmer.","category":"Home & Kitchen","subcategory":"Appliances","price":89.99,"brand":"Instant Pot","tags":"pressure-cooker,kitchen,instant-pot,multi-cooker,cooking,appliance","image_url":"https://images.unsplash.com/photo-1585515320310-259814833e62?w=400&h=400&fit=crop"},
    {"name":"Ninja Air Fryer Max XL","description":"5.5-qt air fryer with Max Crisp Technology reaching 240C. Six cooking functions. Dishwasher-safe parts.","category":"Home & Kitchen","subcategory":"Appliances","price":119.99,"brand":"Ninja","tags":"air-fryer,ninja,kitchen,cooking,healthy,crispy,appliance","image_url":"https://upload.wikimedia.org/wikipedia/commons/d/d3/Air_Fryer_2020.jpg"},
    {"name":"Dyson V15 Detect Vacuum","description":"The most powerful cordless vacuum with laser dust detection and whole-machine HEPA filtration.","category":"Home & Kitchen","subcategory":"Cleaning","price":749.99,"brand":"Dyson","tags":"vacuum,cordless,dyson,cleaning,hepa,powerful,home","image_url":"https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400&h=400&fit=crop"},
    {"name":"Philips Hue Smart Bulbs 4-Pack","description":"16 million colours, works with Alexa, Google Home and Apple HomeKit. Set scenes and schedules via app.","category":"Home & Kitchen","subcategory":"Smart Home","price":59.99,"brand":"Philips","tags":"smart-bulb,philips-hue,smart-home,alexa,colour,lighting,rgb","image_url":"https://images.unsplash.com/photo-1558002038-1055907df827?w=400&h=400&fit=crop"},
    {"name":"IKEA ALEX Drawer Unit","description":"Six smooth-running drawers for home office or bedroom storage. White powder-coated steel frame.","category":"Home & Kitchen","subcategory":"Furniture","price":149.00,"brand":"IKEA","tags":"drawer,furniture,ikea,storage,desk,organiser,white","image_url":"https://images.unsplash.com/photo-1555041469-a586c61ea9bc?w=400&h=400&fit=crop"},
    # Sports
    {"name":"Fitbit Charge 6","description":"Advanced health and fitness tracker with built-in GPS, SpO2, ECG app and Google Maps integration.","category":"Sports","subcategory":"Wearables","price":159.95,"brand":"Fitbit","tags":"fitness-tracker,fitbit,gps,health,heart-rate,wearable,smartwatch","image_url":"https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=400&h=400&fit=crop"},
    {"name":"Bowflex SelectTech 552 Dumbbells","description":"Adjustable dumbbells replacing 15 sets of weights. Dial from 5 to 52.5 lb in seconds. Compact design.","category":"Sports","subcategory":"Weights","price":429.00,"brand":"Bowflex","tags":"dumbbells,weights,bowflex,gym,fitness,strength,home-gym","image_url":"https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=400&h=400&fit=crop"},
    {"name":"Manduka PRO Yoga Mat","description":"6 mm thick premium yoga mat with a lifetime guarantee. Superior non-slip grip and dense cushioning.","category":"Sports","subcategory":"Yoga","price":120.00,"brand":"Manduka","tags":"yoga-mat,manduka,yoga,fitness,non-slip,exercise,meditation","image_url":"https://upload.wikimedia.org/wikipedia/commons/6/6d/Yoga_mat.jpg"},
    {"name":"Garmin Forerunner 255","description":"Running GPS smartwatch with training readiness, daily suggested workouts and up to 14-day battery life.","category":"Sports","subcategory":"Wearables","price":349.99,"brand":"Garmin","tags":"smartwatch,garmin,gps,running,sport,battery,fitness","image_url":"https://images.unsplash.com/photo-1508685096489-7aacd43bd3b1?w=400&h=400&fit=crop"},
    # Books
    {"name":"Atomic Habits by James Clear","description":"Tiny changes, remarkable results. The proven framework for building good habits and breaking bad ones.","category":"Books","subcategory":"Self-Help","price":18.99,"brand":"Avery","tags":"habit,self-help,productivity,psychology,bestseller,non-fiction","image_url":"https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=400&h=400&fit=crop"},
    {"name":"The Psychology of Money","description":"Timeless lessons on wealth, greed, and happiness. Morgan Housel's bestselling personal finance guide.","category":"Books","subcategory":"Finance","price":16.99,"brand":"Harriman House","tags":"finance,money,investing,psychology,personal-finance,non-fiction","image_url":"https://images.unsplash.com/photo-1592496431122-2349e0fbc666?w=400&h=400&fit=crop"},
    {"name":"Dune by Frank Herbert","description":"The epic science fiction masterpiece. A sweeping tale of politics, religion, ecology and power.","category":"Books","subcategory":"Science Fiction","price":14.99,"brand":"Ace","tags":"sci-fi,dune,frank-herbert,epic,fantasy,fiction,classic","image_url":"https://images.unsplash.com/photo-1481627834876-b7833e8f5570?w=400&h=400&fit=crop"},
]

DEMO_USERS = [
    {"username":"alice","email":"alice@demo.com","password":"demo1234","age":28,"gender":"Female","location":"New York"},
    {"username":"bob",  "email":"bob@demo.com",  "password":"demo1234","age":34,"gender":"Male",  "location":"London"},
    {"username":"carol","email":"carol@demo.com","password":"demo1234","age":22,"gender":"Female","location":"Mumbai"},
    {"username":"dave", "email":"dave@demo.com", "password":"demo1234","age":45,"gender":"Male",  "location":"Toronto"},
    {"username":"eve",  "email":"eve@demo.com",  "password":"demo1234","age":31,"gender":"Female","location":"Sydney"},
]

def seed():
    app = create_app()
    with app.app_context():
        db.drop_all()
        db.create_all()

        product_objects = []
        for p in PRODUCTS:
            product_objects.append(Product(
                name=p["name"], description=p["description"],
                category=p["category"], subcategory=p["subcategory"],
                price=p["price"], brand=p["brand"], tags=p["tags"],
                image_url=p["image_url"],
                avg_rating=round(random.uniform(3.5, 5.0), 1),
                reviews_count=random.randint(50, 2000),
                stock=random.randint(10, 500),
            ))
        db.session.add_all(product_objects)
        db.session.commit()
        print(f"✅  Inserted {len(product_objects)} products")

        user_objects = []
        for u in DEMO_USERS:
            user_objects.append(User(
                username=u["username"], email=u["email"],
                password_hash=generate_password_hash(u["password"]),
                age=u["age"], gender=u["gender"], location=u["location"],
            ))
        db.session.add_all(user_objects)
        db.session.commit()
        print(f"✅  Inserted {len(user_objects)} demo users")

        products = Product.query.all()
        users    = User.query.all()

        for user in users:
            for p in random.sample(products, k=random.randint(6, 14)):
                db.session.add(BrowsingHistory(user_id=user.id, product_id=p.id, duration=random.randint(15, 300)))
            for p in random.sample(products, k=random.randint(2, 6)):
                db.session.add(Purchase(user_id=user.id, product_id=p.id, quantity=random.randint(1,3), price_paid=p.price))
            for p in random.sample(products, k=random.randint(4, 10)):
                db.session.add(Rating(user_id=user.id, product_id=p.id, rating=round(random.uniform(2.5, 5.0), 1)))

        db.session.commit()
        print("✅  Inserted synthetic browsing, purchases, and ratings")
        print()
        print("🎉  Database seeded! Demo logins (password: demo1234)")
        for u in DEMO_USERS:
            print(f"   {u['username']:<8}  {u['email']}")

if __name__ == "__main__":
    seed()
