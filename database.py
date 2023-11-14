from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO

def generate_pdf(customer):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    c.drawString(100, height - 100, f"Customer Name: {customer['name']}")
    c.drawString(100, height - 120, f"Mobile Number: {customer['mobile']}")

    y_position = height - 140
    for product in customer.get("products", []):
        c.drawString(100, y_position, f"Product: {product['name']}, Price: {product['price']}")
        y_position -= 20

    c.drawString(100, y_position - 20, f"Total Bill: {sum(p['price'] for p in customer.get('products', []))}")
    c.save()
    buffer.seek(0)
    return buffer


