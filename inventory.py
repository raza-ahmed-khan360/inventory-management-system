# inventory.py
from typing import List, Dict, Type, Optional
from datetime import datetime
from product import Product, Grocery, Electronics, Clothing

class Inventory:
    def __init__(self):
        self._products: Dict[str, Product] = {}

    def add_product(self, product: Product) -> None:
        """Add a product to the inventory."""
        if not isinstance(product, Product):
            raise TypeError("Product must be an instance of Product class")
        if product.product_id in self._products:
            raise ValueError(f"Product with ID '{product.product_id}' already exists.")
        self._products[product.product_id] = product

    def remove_product(self, product_id: str) -> None:
        """Remove a product from the inventory."""
        if product_id not in self._products:
            raise ValueError(f"Product with ID '{product_id}' not found.")
        del self._products[product_id]

    def get_product(self, product_id: str) -> Product:
        """Get a product by its ID."""
        if product_id not in self._products:
            raise ValueError(f"Product with ID '{product_id}' not found.")
        return self._products[product_id]

    def list_all_products(self) -> List[Product]:
        """List all products in the inventory."""
        return list(self._products.values())

    def search_by_name(self, name: str) -> List[Product]:
        """Search products by name (case-insensitive partial match)."""
        return [product for product in self._products.values() 
                if name.lower() in product.name.lower()]

    def search_by_type(self, product_type: Type[Product]) -> List[Product]:
        """Search products by their type (Electronics, Grocery, or Clothing)."""
        return [product for product in self._products.values() 
                if isinstance(product, product_type)]

    def sell_product(self, product_id: str, quantity: int) -> None:
        """Sell a quantity of a product."""
        product = self.get_product(product_id)
        try:
            product.sell(quantity)
        except ValueError as e:
            raise ValueError(f"Error selling product {product_id}: {str(e)}")

    def restock_product(self, product_id: str, quantity: int) -> None:
        """Restock a quantity of a product."""
        product = self.get_product(product_id)
        try:
            product.restock(quantity)
        except ValueError as e:
            raise ValueError(f"Error restocking product {product_id}: {str(e)}")

    def total_inventory_value(self) -> float:
        """Calculate the total value of all products in inventory."""
        return sum(product.get_total_value() for product in self._products.values())

    def remove_expired_products(self) -> List[str]:
        """Remove expired grocery products and return their IDs."""
        current_date = datetime.now().date()
        expired_products = [
            product_id for product_id, product in self._products.items()
            if isinstance(product, Grocery) and product.is_expired()
        ]
        
        for product_id in expired_products:
            del self._products[product_id]
        
        return expired_products

    def get_low_stock_products(self, threshold: int = 5) -> List[Product]:
        """Get products with stock below the specified threshold."""
        return [product for product in self._products.values() 
                if product.quantity_in_stock <= threshold]

    def to_dict_list(self) -> List[dict]:
        """Convert all products to a list of dictionaries for serialization."""
        return [product.to_dict() for product in self._products.values()]
