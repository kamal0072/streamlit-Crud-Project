import sqlite3 
import pandas as pd

# create db connection 
def get_connection():
    conn =  sqlite3.connect(
        'employee.db',
        check_same_thread=False
    )
    return conn

# create employee table

def create_emp_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            department TEXT NOT NULL,
            salary DEC(10, 2) NOT NULL
        )
    """)
    conn.commit()
    conn.close()


# add employee to tha employee table

def add_employee(name, email, department, salary):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
            INSERT INTO employees (name, email, department, salary)
            VALUES (?, ?, ?, ?)
        """,(name, email, department, salary)
    )
    conn.commit()
    conn.close()

# get employees
def get_employees():
    conn = get_connection()

    query = """
        SELECT *FROM employees ORDER BY id DESC
    """
    df = pd.read_sql_query(
        query, 
        conn
    )
    conn.close()
    return df


# get specific/single employees
def get_single_employees(emp_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *FROM employees WHERE id = ?
    """, (emp_id, )
    )
    emp = cursor.fetchone()
    conn.close()
    return emp
     

# update employee Data
def update_employee(emp_id, name, email, department, salary):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """ UPDATE employees 
        SET 
        name=?,email=?, department=?, salary=?
        WHERE id=?
        """, (name, email, department, salary, emp_id)
    )
    conn.commit()
    conn.close()
    return {"msg" : "updated..."}

# delete employee data
def delete_epmloyee_data(emp_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
            DELETE FROM employees WHERE id=?
        """, (emp_id, )
    )
    conn.commit()
    conn.close()

    return {'msg' : 'deleted...'}