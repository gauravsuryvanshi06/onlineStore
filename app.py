import streamlit as st
from database import get_database, add_customer, get_customer_by_mobile, add_product_to_customer
from pdf import generate_pdf

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

