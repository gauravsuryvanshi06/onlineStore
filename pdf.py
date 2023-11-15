# pdf_generator.py
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf(customer):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Ensure customer data is present
    if not customer:
        raise ValueError("No customer data provided")

    # Customer Details
    c.drawString(100, height - 100, f"Customer Name: {customer.get('name', 'N/A')}")
    c.drawString(100, height - 120, f"Mobile Number: {customer.get('mobile', 'N/A')}")

    # Product Details
    y_position = height - 160
    total_bill = 0
    for product in customer.get("products", []):
        product_details = f"{product['name']} - Quantity: {product.get('quantity', 1)} @ Price: {product['price']}"
        c.drawString(100, y_position, product_details)
        total_bill += product.get('quantity', 1) * product['price']
        y_position -= 20

    # Total Bill
    c.drawString(100, y_position - 20, f"Total Bill: {total_bill}")

    c.save()
    buffer.seek(0)
    return buffer
