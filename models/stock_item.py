class StockItem:
    def __init__(self, id=None, name="", category="", quantity=0.0, unit="", min_stock=0.0, last_updated=None):
        self.id = id
        self.name = name
        self.category = category
        self.quantity = quantity
        self.unit = unit
        self.min_stock = min_stock
        self.last_updated = last_updated
    
    def __repr__(self):
        return f"<StockItem(id={self.id}, name='{self.name}', quantity={self.quantity}{self.unit})>"
    
    def is_low_stock(self):
        return self.quantity <= self.min_stock