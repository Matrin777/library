from database.db_manager import get_connection

class Employee:
    def __init__(self, codeemployee=None, name=None, surname=None, telephone=None):
        self.codeemployee = codeemployee
        self.name = name
        self.surname = surname
        self.telephone = telephone
    def save(self):
        conn = get_connection()
        cursor = conn.cursor()
        if self.codeemployee is None:
            cursor.execute("INSERT INTO employee (name, surname, telephone) VALUES (?, ?, ?)", (self.name, self.surname, self.telephone))
            self.codeemployee = cursor.lastrowid
        else:
            cursor.execute("UPDATE employee SET name=?, surname=?, telephone=? WHERE codeemployee=?", (self.name, self.surname, self.telephone, self.codeemployee))
        conn.commit()
        conn.close()
    def delete(self):
        if self.codeemployee:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM employee WHERE codeemployee=?", (self.codeemployee,))
            conn.commit()
            conn.close()
def get_all_employees():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT codeemployee, name, surname, telephone FROM employee")
    rows = cursor.fetchall()
    conn.close()
    return [Employee(codeemployee=row[0], name=row[1], surname=row[2], telephone=row[3]) for row in rows]
def get_employee_by_id(codeemployee):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT codeemployee, name, surname, telephone FROM employee WHERE codeemployee=?", (codeemployee,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Employee(codeemployee=row[0], name=row[1], surname=row[2], telephone=row[3])
    return None