import streamlit as st
import pandas as pd
from datetime import datetime
from inventory import Inventory
from utils import save_inventory_to_file, load_inventory_from_file
from exceptions import ( InvalidProductDataError)
from product import Electronics, Grocery, Clothing

# Initialize session state
if 'inventory' not in st.session_state:
    st.session_state.inventory = Inventory()
    try:
        load_inventory_from_file(st.session_state.inventory, "inventory.json")
    except (FileNotFoundError, InvalidProductDataError) as e:
        st.warning(f"Starting with empty inventory: {str(e)}")

def save_inventory():
    try:
        save_inventory_to_file(st.session_state.inventory, "inventory.json")
        st.success("Inventory saved successfully!")
    except Exception as e:
        st.error(f"Error saving inventory: {str(e)}")

def add_product():
    st.subheader("Add New Product")
    
    # Product type selection
    product_type = st.selectbox(
        "Select Product Type",
        ["Electronics", "Grocery", "Clothing"]
    )
    
    # Common fields for all products
    product_id = st.text_input("Product ID")
    name = st.text_input("Product Name")
    price = st.number_input("Price", min_value=0.0, step=0.01)
    quantity = st.number_input("Quantity", min_value=0, step=1)
    
    # Type-specific fields
    try:
        if product_type == "Electronics":
            brand = st.text_input("Brand")
            warranty_years = st.number_input("Warranty (years)", min_value=0, step=1)
            if st.button("Add Electronics"):
                product = Electronics(product_id, name, price, quantity, brand, warranty_years)
                st.session_state.inventory.add_product(product)
                st.success("Electronics added successfully!")
                save_inventory()
                
        elif product_type == "Grocery":
            expiry_date = st.date_input("Expiry Date")
            if st.button("Add Grocery"):
                product = Grocery(product_id, name, price, quantity, expiry_date.strftime("%Y-%m-%d"))
                st.session_state.inventory.add_product(product)
                st.success("Grocery item added successfully!")
                save_inventory()
                
        elif product_type == "Clothing":
            size = st.text_input("Size")
            material = st.text_input("Material")
            if st.button("Add Clothing"):
                product = Clothing(product_id, name, price, quantity, size, material)
                st.session_state.inventory.add_product(product)
                st.success("Clothing item added successfully!")
                save_inventory()
                
    except Exception as e:
        st.error(f"Error adding product: {str(e)}")

def view_products():
    st.subheader("Current Inventory")
    products = st.session_state.inventory.list_all_products()
    
    if not products:
        st.info("No products in inventory.")
        return
        
    # Convert products to DataFrame for better display
    product_data = []
    for p in products:
        data = {
            'ID': p.product_id,
            'Name': p.name,
            'Type': p.__class__.__name__,
            'Price': f"${p.price:.2f}",
            'Stock': p.quantity_in_stock,
            'Value': f"${p.get_total_value():.2f}"
        }
        if isinstance(p, Electronics):
            data.update({'Brand': p.brand, 'Warranty': f"{p.warranty_years} years"})
        elif isinstance(p, Grocery):
            data.update({'Expiry': p.expiry_date, 'Status': 'Expired' if p.is_expired() else 'Valid'})
        elif isinstance(p, Clothing):
            data.update({'Size': p.size, 'Material': p.material})
        product_data.append(data)
    
    df = pd.DataFrame(product_data)
    st.dataframe(df, use_container_width=True)

def sell_products():
    st.subheader("Sell Products")
    products = st.session_state.inventory.list_all_products()
    if not products:
        st.info("No products available to sell.")
        return
        
    product_dict = {p.product_id: p for p in products}
    product_id = st.selectbox("Select Product", options=list(product_dict.keys()),
                            format_func=lambda x: f"{product_dict[x].name} (ID: {x})")
    
    if product_id:
        product = product_dict[product_id]
        st.write(f"Available stock: {product.quantity_in_stock}")
        quantity = st.number_input("Quantity to sell", min_value=1, max_value=product.quantity_in_stock)
        
        if st.button("Complete Sale"):
            try:
                st.session_state.inventory.sell_product(product_id, quantity)
                st.success(f"Successfully sold {quantity} units of {product.name}")
                save_inventory()
            except Exception as e:
                st.error(f"Error completing sale: {str(e)}")

def restock_products():
    st.subheader("Restock Products")
    products = st.session_state.inventory.list_all_products()
    if not products:
        st.info("No products available to restock.")
        return
        
    product_dict = {p.product_id: p for p in products}
    product_id = st.selectbox("Select Product", options=list(product_dict.keys()),
                            format_func=lambda x: f"{product_dict[x].name} (ID: {x})")
    
    if product_id:
        product = product_dict[product_id]
        st.write(f"Current stock: {product.quantity_in_stock}")
        quantity = st.number_input("Quantity to add", min_value=1)
        
        if st.button("Restock"):
            try:
                st.session_state.inventory.restock_product(product_id, quantity)
                st.success(f"Successfully added {quantity} units to stock")
                save_inventory()
            except Exception as e:
                st.error(f"Error restocking: {str(e)}")

def search_products():
    st.subheader("Search Products")
    search_type = st.radio("Search by", ["Name", "Product Type"])
    
    try:
        if search_type == "Name":
            name = st.text_input("Enter product name")
            if name:
                results = st.session_state.inventory.search_by_name(name)
                if results:
                    product_data = []
                    for p in results:
                        data = {
                            'ID': p.product_id,
                            'Name': p.name,
                            'Type': p.__class__.__name__,
                            'Price': f"${p.price:.2f}",
                            'Stock': p.quantity_in_stock
                        }
                        product_data.append(data)
                    st.dataframe(pd.DataFrame(product_data), use_container_width=True)
                else:
                    st.info("No products found.")
        else:
            product_type = st.selectbox("Select Product Type", 
                                      ["Electronics", "Grocery", "Clothing"])
            type_map = {
                "Electronics": Electronics,
                "Grocery": Grocery,
                "Clothing": Clothing
            }
            results = st.session_state.inventory.search_by_type(type_map[product_type])
            if results:
                product_data = []
                for p in results:
                    data = {
                        'ID': p.product_id,
                        'Name': p.name,
                        'Price': f"${p.price:.2f}",
                        'Stock': p.quantity_in_stock
                    }
                    product_data.append(data)
                st.dataframe(pd.DataFrame(product_data), use_container_width=True)
            else:
                st.info(f"No {product_type} products found.")
    except Exception as e:
        st.error(f"Error searching products: {str(e)}")

def remove_expired():
    st.subheader("Remove Expired Products")
    if st.button("Remove All Expired Products"):
        try:
            expired_products = st.session_state.inventory.remove_expired_products()
            if expired_products:
                st.success(f"Removed {len(expired_products)} expired products")
                save_inventory()
            else:
                st.info("No expired products found")
        except Exception as e:
            st.error(f"Error removing expired products: {str(e)}")

def main():
    st.title("Inventory Management System")
    
    # Sidebar menu
    menu = st.sidebar.selectbox(
        "Menu",
        ["View Inventory", "Add Product", "Sell Product", "Restock Product", 
         "Search Products", "Remove Expired", "Save Inventory"]
    )
    
    if menu == "View Inventory":
        view_products()
        total_value = st.session_state.inventory.total_inventory_value()
        st.metric("Total Inventory Value", f"${total_value:.2f}")
        
    elif menu == "Add Product":
        add_product()
        
    elif menu == "Sell Product":
        sell_products()
        
    elif menu == "Restock Product":
        restock_products()
        
    elif menu == "Search Products":
        search_products()
        
    elif menu == "Remove Expired":
        remove_expired()
        
    elif menu == "Save Inventory":
        if st.button("Save Current Inventory"):
            save_inventory()

if __name__ == "__main__":
    main()
