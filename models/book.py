from database.db_manager import get_connection

class Book:
    def __init__(self, codebook=None, name=None, author_code=None, price=None, codeganre=None):
        self.codebook = codebook
        self.name = name
        self.author_code = author_code
        self.price = price
        self.codeganre = codeganre
    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.codebook is None:
            cursor.execute(
                "INSERT INTO book (name, author_code, price, codeganre) VALUES (?, ?, ?, ?)",
                (self.name, self.author_code, self.price, self.codeganre)
            )
            self.codebook = cursor.lastrowid
        else:
            cursor.execute(
                "UPDATE book SET name=?, author_code=?, price=?, codeganre=? WHERE codebook=?",
                (self.name, self.author_code, self.price, self.codeganre, self.codebook)
            )
        conn.commit()
        conn.close()
    def delete(self):
        if self.codebook:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM book WHERE codebook=?", (self.codebook,))
            conn.commit()
            conn.close()
def get_all_books():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT codebook, name, author_code, price, codeganre FROM book")
    rows = cursor.fetchall()
    conn.close()
    return [Book(
        codebook=row[0],
        name=row[1],
        author_code=row[2],
        price=row[3],
        codeganre=row[4]
    ) for row in rows]
def get_book_by_code(codebook):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT codebook, name, author_code, price, codeganre FROM book WHERE codebook=?", (codebook,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Book(
            codebook=row[0],
            name=row[1],
            author_code=row[2],
            price=row[3],
            codeganre=row[4]
        )
    return None