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
    
def aggregate_product_data(db):
    pipeline = [
        {"$unwind": "$products"},  # Unwind the products array
        {"$group": {
            "_id": "$products.name",  # Group by product name
            "total_quantity": {"$sum": "$products.quantity"}  # Sum the quantity for each product
        }},
        {"$sort": {"total_quantity": -1}}  # Sort by total quantity in descending order
    ]
    return list(db.customers.aggregate(pipeline))



def categorize_product_demand(sales_data):
    # Define thresholds for high, medium, and low demand
    high_demand_threshold = 100  # Example value, adjust as needed
    medium_demand_threshold = 50  # Example value, adjust as needed

    categorized_data = {
        "high_demand": [],
        "medium_demand": [],
        "low_demand": []
    }

    for product in sales_data:
        if product['total_quantity_sold'] >= high_demand_threshold:
            categorized_data['high_demand'].append(product['_id'])
        elif product['total_quantity_sold'] >= medium_demand_threshold:
            categorized_data['medium_demand'].append(product['_id'])
        else:
            categorized_data['low_demand'].append(product['_id'])

    return categorized_data
