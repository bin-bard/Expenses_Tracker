import sqlite3

# Connect to the database
conn = sqlite3.connect('expense.db')
c = conn.cursor()

# Create table
c.execute('''
    CREATE TABLE IF NOT EXISTS expenses (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Expense_Name TEXT,
        Category TEXT,
        Cost REAL,
        Time TEXT
    )
''')

c.execute('''
    CREATE TABLE IF NOT EXISTS balance (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Balance_time TEXT,
        Balance REAL
    )
''')

# Commit the changes
conn.commit()


def insert_groceries(Expense_Name, Category, Cost, Time):
    INSERT_EXPENSES = "INSERT INTO expenses (Expense_Name, Category, Cost, Time) VALUES (?, ?, ?, ?)"
    c.execute(INSERT_EXPENSES, (Expense_Name, Category, Cost, Time))
    conn.commit()

def insert_balance(balance, time):
    INSERT_BALANCE = "INSERT INTO balance (Balance, Balance_time) VALUES (?,?)"
    c.execute(INSERT_BALANCE, (balance,time))
    conn.commit()

def select_balance():
    SELECT_LAST_ROW = "SELECT Balance FROM balance ORDER BY ID DESC LIMIT 1"
    c.execute(SELECT_LAST_ROW)
    result = c.fetchone()
    return result[0] if result is not None else 0

def select_all():
    SELECT_ALL = "SELECT *  FROM expenses"
    c.execute(SELECT_ALL)
    return [list(row) for row in c.fetchall()]

def delete_one(ID):
    DELETE_ONE = "DELETE FROM expenses WHERE ID = ?"
    c.execute(DELETE_ONE, (ID,))
    conn.commit()

def sum_all():
    SUM_ALL = "SELECT SUM(Cost) FROM expenses"
    c.execute(SUM_ALL)
    return c.fetchone()[0]