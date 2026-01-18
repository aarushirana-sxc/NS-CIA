import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            table_number TEXT NOT NULL,
            items TEXT NOT NULL,
            order_time TEXT NOT NULL,
            status TEXT DEFAULT 'Pending'
        )
    ''')
    conn.commit()
    conn.close()

def save_order(table_num, items):
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    time_now = datetime.now().strftime("%H:%M:%S")
    cursor.execute('INSERT INTO orders (table_number, items, order_time) VALUES (?, ?, ?)', 
                   (table_num, items, time_now))
    conn.commit()
    order_id = cursor.lastrowid
    conn.close()
    return f"Order #{order_id} Confirmed"

def mark_order_done(order_id):
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    
    # Check if order exists first
    cursor.execute('SELECT * FROM orders WHERE id = ?', (order_id,))
    if not cursor.fetchone():
        conn.close()
        return "Order ID not found."

    cursor.execute("UPDATE orders SET status = 'Completed' WHERE id = ?", (order_id,))
    conn.commit()
    conn.close()
    return f"Order #{order_id} marked as COMPLETED."

def get_kitchen_view():
    # shows active orders with status 'Pending'
    conn = sqlite3.connect('restaurant.db')
    cursor = conn.cursor()
    
    # CHANGED: We now filter by status='Pending'
    cursor.execute("SELECT id, table_number, items FROM orders WHERE status='Pending'")
    rows = cursor.fetchall()
    conn.close()
    
    if not rows:
        return "No Pending Orders. Kitchen Clear!"
    
    display = "--- ACTIVE ORDERS ---\n"
    for r in rows:
        display += f"[ID: {r[0]}] Table {r[1]}: {r[2]}\n"
    return display

init_db()