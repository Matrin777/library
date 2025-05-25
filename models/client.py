from database.db_manager import get_connection

class Client:
    def __init__(self, codeclient=None, name=None, surname=None, telephone=None):
        self.codeclient = codeclient
        self.name = name
        self.surname = surname
        self.telephone = telephone
    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.codeclient is None:
            cursor.execute("INSERT INTO client (name, surname, telephone) VALUES (?, ?, ?)", (self.name, self.surname, self.telephone))
            self.codeclient = cursor.lastrowid
        else:
            cursor.execute("UPDATE client SET name=?, surname=?, telephone=? WHERE codeclient=?", (self.name, self.surname, self.telephone, self.codeclient))
        conn.commit()
        conn.close()
    def delete(self):
        if self.codeclient:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM client WHERE codeclient=?", (self.codeclient,))
            conn.commit()
            conn.close()
def get_all_clients():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT codeclient, name, surname, telephone FROM client")
    rows = cursor.fetchall()
    conn.close()
    return [Client(codeclient=row[0], name=row[1], surname=row[2], telephone=row[3]) for row in rows]

def get_client_by_id(codeclient):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT codeclient, name, surname, telephone FROM client WHERE codeclient=?", (codeclient,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Client(codeclient=row[0], name=row[1], surname=row[2], telephone=row[3])
    return None