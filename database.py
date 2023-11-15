from pymongo import MongoClient
from urllib.parse import quote_plus

username = "online"  # Replace with your actual username
password = "Gaurav@321"  # Replace with your actual password

escaped_username = quote_plus(username)
escaped_password = quote_plus(password)

uri = f"mongodb+srv://{escaped_username}:{escaped_password}@online.ol4zd0a.mongodb.net/onlinr?retryWrites=true&w=majority"

client = MongoClient(uri)

def get_database():
    connection_string = "mongodb://atlas-sql-649f109d3916b8466dca1fc0-45hpj.a.query.mongodb.net/mongodbVSCodePlaygroundDB?ssl=true&authSource=admin"
    client = MongoClient(uri)
    return client['online']

def add_customer(db, name, mobile):
    db.customers.insert_one({"name": name, "mobile": mobile})

def get_customer_by_mobile(db, mobile):
    return db.customers.find_one({"mobile": mobile})

def add_product_to_customer(db, mobile, product, price):
    db.customers.update_one({"mobile": mobile}, {"$push": {"products": {"name": product, "price": price}}})
    
def aggregate_product_sales(db):
    # This pipeline aggregates the total quantity sold for each product
    pipeline = [
        {"$unwind": "$products"},  # Unwinds the products array
        {"$group": {
            "_id": "$products.name",  # Groups by product name
            "total_quantity_sold": {"$sum": "$products.quantity"}  # Sums up the quantity for each product
        }},
        {"$sort": {"total_quantity_sold": -1}}  # Sorts the result by total quantity sold in descending order
    ]
    return list(db.customers.aggregate(pipeline))
