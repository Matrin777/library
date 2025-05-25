from database.db_manager import get_connection

class Genre:
    def __init__(self, codeganre=None, name=None):
        self.codeganre = codeganre
        self.name = name

    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.codeganre is None:
            cursor.execute("INSERT INTO ganre (name) VALUES (?)", (self.name,))
            self.codeganre = cursor.lastrowid
        else:
            cursor.execute("UPDATE ganre SET name=? WHERE codeganre=?", (self.name, self.codeganre))
        conn.commit()
        conn.close()

    def delete(self):
        if self.codeganre:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM ganre WHERE codeganre=?", (self.codeganre,))
            conn.commit()
            conn.close()

def get_all_genres():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT codeganre, name FROM ganre")
    rows = cursor.fetchall()
    conn.close()
    return [Genre(codeganre=row[0], name=row[1]) for row in rows]

def get_genre_by_id(codeganre):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT codeganre, name FROM ganre WHERE codeganre=?", (codeganre,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Genre(codeganre=row[0], name=row[1])
    return None

def initialize_genres():
    genres = ["Фантастика", "Боевик", "Анекдот", "Наука", "Роман", "История"]
    existing = get_all_genres()
    existing_names = [g.name for g in existing]
    for name in genres:
        if name not in existing_names:
            g = Genre(name=name)
            g.save()