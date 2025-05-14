from abc import ABC, abstractmethod
from datetime import datetime

class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, quantity_in_stock: int):
        self._product_id = product_id
        self._name = name
        if price < 0:
            raise ValueError("Price cannot be negative")
        self._price = price
        if quantity_in_stock < 0:
            raise ValueError("Quantity cannot be negative")
        self._quantity_in_stock = quantity_in_stock

    @property
    def product_id(self):
        return self._product_id

    @property
    def name(self):
        return self._name

    @property
    def price(self):
        return self._price

    @property
    def quantity_in_stock(self):
        return self._quantity_in_stock

    def restock(self, amount: int) -> None:
        if amount <= 0:
            raise ValueError("Restock amount must be positive")
        self._quantity_in_stock += amount

    def sell(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Sell quantity must be positive")
        if quantity > self._quantity_in_stock:
            raise ValueError(f"Not enough stock available. Current stock: {self._quantity_in_stock}")
        self._quantity_in_stock -= quantity

    def get_total_value(self) -> float:
        return self._price * self._quantity_in_stock

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        return {
            'product_id': self._product_id,
            'name': self._name,
            'price': self._price,
            'quantity_in_stock': self._quantity_in_stock,
            'type': self.__class__.__name__
        }

class Electronics(Product):
    def __init__(self, product_id: str, name: str, price: float, quantity_in_stock: int, 
                 brand: str, warranty_years: int):
        super().__init__(product_id, name, price, quantity_in_stock)
        self._brand = brand
        if warranty_years < 0:
            raise ValueError("Warranty years cannot be negative")
        self._warranty_years = warranty_years

    @property
    def brand(self):
        return self._brand

    @property
    def warranty_years(self):
        return self._warranty_years

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            'brand': self._brand,
            'warranty_years': self._warranty_years
        })
        return data

    def __str__(self) -> str:
        return f"Electronics: {self._name} (ID: {self._product_id}) - ${self._price:.2f}\n" \
               f"Brand: {self._brand} | Warranty: {self._warranty_years} years | Stock: {self._quantity_in_stock}"

class Grocery(Product):
    def __init__(self, product_id: str, name: str, price: float, quantity_in_stock: int, 
                 expiry_date: str):
        super().__init__(product_id, name, price, quantity_in_stock)
        self._expiry_date = expiry_date

    @property
    def expiry_date(self):
        return self._expiry_date

    def is_expired(self) -> bool:
        current_date = datetime.now().date()
        expiry_date = datetime.strptime(self._expiry_date, "%Y-%m-%d").date()
        return current_date > expiry_date

    def to_dict(self) -> dict:
        data = super().to_dict()
        data['expiry_date'] = self._expiry_date
        return data

    def __str__(self) -> str:
        status = "EXPIRED" if self.is_expired() else "Valid"
        return f"Grocery: {self._name} (ID: {self._product_id}) - ${self._price:.2f}\n" \
               f"Expiry Date: {self._expiry_date} | Status: {status} | Stock: {self._quantity_in_stock}"

class Clothing(Product):
    def __init__(self, product_id: str, name: str, price: float, quantity_in_stock: int, 
                 size: str, material: str):
        super().__init__(product_id, name, price, quantity_in_stock)
        self._size = size
        self._material = material

    @property
    def size(self):
        return self._size

    @property
    def material(self):
        return self._material

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({
            'size': self._size,
            'material': self._material
        })
        return data

    def __str__(self) -> str:
        return f"Clothing: {self._name} (ID: {self._product_id}) - ${self._price:.2f}\n" \
               f"Size: {self._size} | Material: {self._material} | Stock: {self._quantity_in_stock}"
