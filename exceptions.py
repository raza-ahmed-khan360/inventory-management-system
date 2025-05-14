class InventoryError(Exception):
    """Base class for inventory management system exceptions."""
    pass

class InsufficientStockError(InventoryError):
    """Raised when attempting to sell more items than available in stock."""
    pass

class DuplicateProductError(InventoryError):
    """Raised when attempting to add a product with an ID that already exists."""
    pass

class ProductNotFoundError(InventoryError):
    """Raised when attempting to access a product that doesn't exist."""
    pass

class InvalidProductDataError(InventoryError):
    """Raised when loading invalid product data from file."""
    pass

class NegativeValueError(InventoryError):
    """Raised when attempting to set a negative value for price or quantity."""
    pass
