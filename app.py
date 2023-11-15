import streamlit as st
from database import get_database, add_customer, get_customer_by_mobile, add_product_to_customer
from pdf import generate_pdf
from database import aggregate_product_sales, categorize_product_demand, get_all_customers_data
import pandas as pd
db = get_database()

st.title("Online Merch Grocery Store")

# Customer addition
with st.form("add_customer"):
    name = st.text_input("Customer Name")
    mobile = st.text_input("Mobile Number")
    submitted = st.form_submit_button("Add Customer")
    if submitted:
        add_customer(db, name, mobile)
        st.success("Customer Added")

# Product selection
products = {"salt": 1, "peanuts": 2, "Nirama": 3, "Mango": 4}
customer_mobile = st.text_input("Enter Customer Mobile to Add Products")

with st.form("add_products"):
    selected_product = st.selectbox("Select Product", list(products.keys()))
    add_product = st.form_submit_button("Add Product")
    if add_product:
        add_product_to_customer(db, customer_mobile, selected_product, products[selected_product])
        st.success("Product Added")

if st.button("Generate Bill"):
    customer = get_customer_by_mobile(db, customer_mobile)
    if customer:
        pdf_file = generate_pdf(customer)

        # Convert BytesIO to bytes for download
        pdf_bytes = pdf_file.getvalue()
        st.download_button(
            label="Download PDF",
            data=pdf_bytes,
            file_name="grocery_bill.pdf",
            mime="application/pdf"
        )
    else:
        st.error("Customer not found. Please check the mobile number.")

# ... your existing Streamlit app code ...
# ... other code ...
if st.button("Refresh Data"):
    sales_data = aggregate_product_sales(db)
    # rest of the code to display the data

if st.button("Analyze Product Demand"):
    sales_data = aggregate_product_sales(db)
    demand_analysis = categorize_product_demand(sales_data)

    # Display the analysis and sales data
    # ... code to display demand analysis ...

    st.subheader("Quantity-wise Selling of Products")
    try:
        sales_df = pd.DataFrame(sales_data)
        if not sales_df.empty:
            sales_df.rename(columns={'_id': 'Product', 'total_quantity_sold': 'Total Sold'}, inplace=True)
            st.table(sales_df)
        else:
            st.write("No sales data available.")
    except NameError:
        st.error("Pandas is not installed or not imported correctly.")
st.write("Customer Purchase Data")

if st.button("Show Customer Data"):
    customer_data = get_all_customers_data(db)
    if customer_data:
        for customer in customer_data:
            st.subheader(f"Customer: {customer['name']} - Mobile: {customer['mobile']}")
            for product in customer['products']:
                st.write(f"Product: {product['name']}, Quantity: {product.get('quantity', 1)}")
    else:
        st.write("No customer data available.")
