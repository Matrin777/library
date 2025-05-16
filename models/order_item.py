from database.db_manager import get_connection

class OrderItem:
    def __init__(self, id=None, order_id=None, product_id=None, quantity=1, item_price=0.0):
        self.id = id
        self.order_id = order_id
        self.product_id = product_id
        self.quantity = quantity
        self.item_price = item_price
    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                "INSERT INTO issue_details (date, codeissuance, codebook, quantity, price) VALUES (?, ?, ?, ?, ?)",
                (None, self.order_id, self.product_id, self.quantity, self.item_price)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE issue_details SET date=?, codeissuance=?, codebook=?, quantity=?, price=? WHERE codeissuedetails=?",
                (None, self.order_id, self.product_id, self.quantity, self.item_price, self.id)
            )
        conn.commit()
        conn.close()
    def delete(self):
        if self.id:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM issue_details WHERE codeissuedetails=?", (self.id,))
            conn.commit()
            conn.close()
def get_items_by_order_id(order_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT codeissuedetails, date, codeissuance, codebook, quantity, price FROM issue_details WHERE codeissuance=?", (order_id,))
    rows = cursor.fetchall()
    conn.close()
    return [OrderItem(id=row[0], order_id=row[2], product_id=row[3], quantity=row[4], item_price=row[5]) for row in rows]
def get_product_by_id(product_id):
    from models import book
    return book.get_book_by_code(product_id)