from database.db_manager import get_connection

class Author:
    def __init__(self, codeauthor=None, name=None, surname=None):
        self.codeauthor = codeauthor
        self.name = name
        self.surname = surname
    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.codeauthor is None:
            cursor.execute("INSERT INTO author (name, surname) VALUES (?, ?)", (self.name, self.surname))
            self.codeauthor = cursor.lastrowid
        else:
            cursor.execute("UPDATE author SET name=?, surname=? WHERE codeauthor=?", (self.name, self.surname, self.codeauthor))
        conn.commit()
        conn.close()
    def delete(self):
        if self.codeauthor:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM author WHERE codeauthor=?", (self.codeauthor,))
            conn.commit()
            conn.close()
def get_all_authors():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT codeauthor, name, surname FROM author")
    rows = cursor.fetchall()
    conn.close()
    return [Author(codeauthor=row[0], name=row[1], surname=row[2]) for row in rows]
def get_author_by_id(codeauthor):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT codeauthor, name, surname FROM author WHERE codeauthor=?", (codeauthor,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Author(codeauthor=row[0], name=row[1], surname=row[2])
    return None