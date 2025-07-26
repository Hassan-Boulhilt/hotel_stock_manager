import sqlite3
import os
from models.stock_item import StockItem

class DatabaseManager:
    def __init__(self):
        db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'hotel_stock.db')
        self.conn = sqlite3.connect(db_path)
        self.create_tables()
    
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                quantity REAL NOT NULL,
                unit TEXT NOT NULL,
                min_stock REAL NOT NULL,
                last_updated TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def add_stock_item(self, item):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO stock_items (name, category, quantity, unit, min_stock)
            VALUES (?, ?, ?, ?, ?)
        ''', (item.name, item.category, item.quantity, item.unit, item.min_stock))
        self.conn.commit()
        return cursor.lastrowid
    
    def update_stock_item(self, item):
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE stock_items 
            SET name=?, category=?, quantity=?, unit=?, min_stock=?
            WHERE id=?
        ''', (item.name, item.category, item.quantity, item.unit, item.min_stock, item.id))
        self.conn.commit()
    
    def delete_stock_item(self, item_id):
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM stock_items WHERE id=?', (item_id,))
        self.conn.commit()
    
    def get_all_items(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM stock_items')
        return [StockItem(*row) for row in cursor.fetchall()]
    
    def get_item_by_id(self, item_id):
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM stock_items WHERE id=?', (item_id,))
        row = cursor.fetchone()
        return StockItem(*row) if row else None
    
    def close(self):
        self.conn.close()