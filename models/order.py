from database.db_manager import get_connection

class Order:
    def __init__(self, id=None, client_id=None, total_amount=0.0, order_date=None):
        self.id = id
        self.client_id = client_id
        self.total_amount = total_amount
        self.order_date = order_date
    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.id is None:
            cursor.execute(
                "INSERT INTO issuance (data, codeclient, codeemployee) VALUES (?, ?, ?)",
                (self.order_date, self.client_id, None)
            )
            self.id = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE issuance SET data=?, codeclient=?, codeemployee=? WHERE codeissuance=?",
                (self.order_date, self.client_id, None, self.id)
            )
        conn.commit()
        conn.close()
    def delete(self):
        if self.id:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM issuance WHERE codeissuance=?", (self.id,))
            conn.commit()
            conn.close()
def get_all_orders():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT codeissuance, data, codeclient, codeemployee FROM issuance")
    rows = cursor.fetchall()
    conn.close()
    return [Order(id=row[0], order_date=row[1], client_id=row[2]) for row in rows]
def get_order_by_id(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT codeissuance, data, codeclient, codeemployee FROM issuance WHERE codeissuance=?", (id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Order(id=row[0], order_date=row[1], client_id=row[2])
    return None