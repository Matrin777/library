import sqlite3
from config import DB_NAME
def get_connection():
    return sqlite3.connect(DB_NAME)
def initialize_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS author (
            codeauthor INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL)
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS ganre (
            codeganre INTEGER PRIMARY KEY,
            name TEXT)
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employee (
            codeemployee INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            telephone TEXT)
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS client (
            codeclient INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            surname TEXT NOT NULL,
            telephone TEXT)
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS book (
            codebook INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            author_code INTEGER,
            price REAL,
            codeganre INTEGER,
            FOREIGN KEY (author_code) REFERENCES author(codeauthor),
            FOREIGN KEY (codeganre) REFERENCES ganre(codeganre))
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS issuance (
            codeissuance INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL,
            codeclient INTEGER,
            codeemployee INTEGER,
            FOREIGN KEY (codeclient) REFERENCES client(codeclient),
            FOREIGN KEY (codeemployee) REFERENCES employee(codeemployee))
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS issue_details (
            codeissuedetails INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            codeissuance INTEGER,
            codebook INTEGER,
            quantity INTEGER NOT NULL,
            price REAL NOT NULL,
            FOREIGN KEY (codeissuance) REFERENCES issuance(codeissuance),
            FOREIGN KEY (codebook) REFERENCES book(codebook))
    ''')

    conn.commit()
    conn.close()