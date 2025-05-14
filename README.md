# Inventory Management System

A Python-based inventory management system with a Streamlit web interface for managing products of different types (Electronics, Grocery, and Clothing).

## Features

- **Product Management**
  - Add new products (Electronics, Grocery, Clothing)
  - Remove products
  - Update stock levels
  - Track product details and specifications

- **Inventory Operations**
  - Track stock levels
  - Sell products
  - Restock products
  - Calculate total inventory value
  - Remove expired grocery items
  - Monitor low stock products

- **Search and Filter**
  - Search products by name
  - Filter products by type
  - View low stock items

## Installation

1. Clone the repository
2. Install the required dependencies:
```
pip install -r requirements.txt
```

## Usage

1. Start the application:
```
streamlit run app.py
```

2. Use the sidebar menu to navigate different features:
   - View Inventory
   - Add Product
   - Sell Product
   - Restock Product
   - Search Products
   - Remove Expired Products
   - Save Inventory

## Product Types

### Electronics
- Product ID
- Name
- Price
- Quantity in stock
- Brand
- Warranty period

### Grocery
- Product ID
- Name
- Price
- Quantity in stock
- Expiry date

### Clothing
- Product ID
- Name
- Price
- Quantity in stock
- Size
- Material

## Data Storage

The inventory data is stored in a JSON file (`inventory.json`) which is automatically loaded when the application starts and can be saved through the interface.

## Error Handling

The system includes comprehensive error handling for:
- Invalid product data
- Insufficient stock
- Duplicate products
- Product not found
- Negative values for price/quantity

## Requirements

- Python 3.x
- Streamlit
- Pandas