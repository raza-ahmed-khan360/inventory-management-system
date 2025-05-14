import json
from typing import List, Dict, Any
from datetime import datetime

from product import Product, Clothing, Electronics, Grocery
from inventory import Inventory
from exceptions import InvalidProductDataError, DuplicateProductError

def save_inventory_to_file(inventory: Inventory, filename: str) -> None:
    """Save inventory data to a JSON file.
    
    Args:
        inventory: The Inventory instance to save
        filename: Path to the JSON file
    
    Raises:
        IOError: If there's an error writing to the file
    """
    try:
        with open(filename, 'w') as f:
            inventory_data = inventory.to_dict_list()
            json.dump(inventory_data, f, indent=4)
    except IOError as e:
        raise IOError(f"Failed to save inventory to {filename}: {str(e)}")

def load_inventory_from_file(inventory: Inventory, filename: str) -> None:
    """Load inventory data from a JSON file.
    
    Args:
        inventory: The Inventory instance to load into
        filename: Path to the JSON file
    
    Raises:
        FileNotFoundError: If the file doesn't exist
        InvalidProductDataError: If the JSON data is invalid
        DuplicateProductError: If a product with same ID already exists
    """
    try:
        with open(filename, 'r') as f:
            inventory_data = json.load(f)
            
        for product_data in inventory_data:
            try:
                # Validate required fields
                required_fields = ['product_id', 'name', 'price', 'quantity_in_stock', 'type']
                if not all(field in product_data for field in required_fields):
                    raise InvalidProductDataError(
                        f"Missing required fields in product data: {product_data}")
                
                # Create the appropriate product instance based on type
                product_type = product_data.pop('type')  # Remove type field before creating instance
                if product_type == "Electronics":
                    if not all(field in product_data for field in ['brand', 'warranty_years']):
                        raise InvalidProductDataError("Missing Electronics-specific fields")
                    product = Electronics(**product_data)
                elif product_type == "Grocery":
                    if 'expiry_date' not in product_data:
                        raise InvalidProductDataError("Missing Grocery-specific fields")
                    product = Grocery(**product_data)
                elif product_type == "Clothing":
                    if not all(field in product_data for field in ['size', 'material']):
                        raise InvalidProductDataError("Missing Clothing-specific fields")
                    product = Clothing(**product_data)
                else:
                    raise InvalidProductDataError(f"Unknown product type: {product_type}")
                
                inventory.add_product(product)
                
            except (ValueError, TypeError) as e:
                raise InvalidProductDataError(f"Invalid product data: {str(e)}")
            except DuplicateProductError:
                # Re-raise DuplicateProductError from inventory.add_product
                raise
                
    except FileNotFoundError:
        # It's okay if the file doesn't exist on first run
        pass
    except json.JSONDecodeError as e:
        raise InvalidProductDataError(f"Invalid JSON format in {filename}: {str(e)}")
    except Exception as e:
        raise InvalidProductDataError(f"Unexpected error loading inventory: {str(e)}")

def create_product_from_input() -> Product:
    """Helper function to create a product instance from user input.
    
    Returns:
        Product: A new product instance
        
    Raises:
        ValueError: If invalid input is provided
    """
    product_types = {
        '1': ('Electronics', Electronics),
        '2': ('Grocery', Grocery),
        '3': ('Clothing', Clothing)
    }
    
    print("\nProduct Types:")
    for key, (name, _) in product_types.items():
        print(f"{key}. {name}")
    
    type_choice = input("Enter product type (1-3): ")
    if type_choice not in product_types:
        raise ValueError("Invalid product type selected")
    
    product_type_name, product_class = product_types[type_choice]
    
    # Get common product attributes
    product_id = input("Enter product ID: ")
    name = input("Enter product name: ")
    price = float(input("Enter price: "))
    quantity = int(input("Enter quantity: "))
    
    # Get type-specific attributes
    if product_type_name == 'Electronics':
        brand = input("Enter brand: ")
        warranty_years = int(input("Enter warranty years: "))
        return Electronics(product_id, name, price, quantity, brand, warranty_years)
    elif product_type_name == 'Grocery':
        expiry_date = input("Enter expiry date (YYYY-MM-DD): ")
        # Validate date format
        try:
            datetime.strptime(expiry_date, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format. Use YYYY-MM-DD")
        return Grocery(product_id, name, price, quantity, expiry_date)
    else:  # Clothing
        size = input("Enter size: ")
        material = input("Enter material: ")
        return Clothing(product_id, name, price, quantity, size, material)
