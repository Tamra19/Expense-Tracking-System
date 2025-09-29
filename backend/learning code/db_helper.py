"""
***********************THIS IS SHOWING ERRORS, FIX THEM LATER**************************
CRUD- Create, Retrieve, Update, Delete
TDD- Test Driven Development (writing tests before any function to fail, then writing the function after unit testing)
"""
import mysql.connector
from contextlib import contextmanager
from logging_setup import setup_logger

logger = setup_logger('db_helper')

#modularizing the code using generator and contextlib
@contextmanager
def get_db_cursor(commit=False):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="expense_manager"
    )


    cursor = connection.cursor(dictionary=True)
    yield cursor

    #when you want to insert a row in a table, you use commit
    if commit:
        connection.commit()
    else:
        pass

    cursor.close()
    connection.close()

def fetch_all_records():
    #retrieving data from db
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM expenses")
        expenses = cursor.fetchall()

        for expense in expenses:
            print(expense)


def fetch_expenses_for_date(expense_date):
    logger.info(f"fetch_expenses_for_date called with {expense_date}")
    with get_db_cursor() as cursor: # if you don't write anything between parenthesis, it returns a tuple
        cursor.execute("SELECT amount, category, notes FROM expenses WHERE expense_date = %s", (expense_date,))
        #why was this showing error when (expense_date) was written instead of (expense_date,)
        rows = cursor.fetchall()
        # Force conversion into dicts with only needed keys
        """
        expenses = [
            {"amount": row["amount"], "category": row["category"], "notes": row["notes"]}
            for row in rows
        ]
        """
        # Force only the fields your model needs
        expenses = []
        for row in rows:
            expenses.append({
                "amount": row["amount"],
                "category": row["category"],
                "notes": row["notes"]
            })
        #print(rows)
        return expenses

def insert_expense(expense_date, amount, category, notes):
    logger.info(f"insert_expense called with date: {expense_date}, amount: {amount}, category: {category}, notes: {notes}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute(
            "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)",
            (expense_date, amount, category, notes)
        )

def delete_expenses_for_date(expense_date):
    logger.info(f"delete_expenses_for_date called with {expense_date}")
    with get_db_cursor(commit=True) as cursor:
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))
        print(f"record(s) with date {(expense_date,)} deleted")

def fetch_expense_summary(start_date, end_date):
    logger.info(f"fetch_expense_summary with start: {start_date} and end: {end_date}")
    with get_db_cursor() as cursor:
        cursor.execute(
            '''SELECT category, SUM(amount) as total
               FROM expenses
               WHERE expense_date
               BETWEEN %s AND %s
               GROUP BY category;''',
    (start_date,end_date)
        )
        data = cursor.fetchall()
        return data

#using delete and update function as one instead as two separate functions
# In db_helper.py

# ... (keep get_db_cursor and other functions as they are for other uses) ...

def add_or_update_expenses_transaction(expense_date, expenses):
    logger.info(f"add_or_update with date: {expense_date} and expenses. )")
    """
    Deletes all expenses for a given date and inserts a new list
    within a single, atomic database transaction.
    """
    connection = None
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="expense_manager"
        )
        cursor = connection.cursor()

        # 1. Delete existing records
        cursor.execute("DELETE FROM expenses WHERE expense_date = %s", (expense_date,))

        # 2. Prepare data for batch insert
        insert_data = [
            (expense_date, expense.amount, expense.category, expense.notes)
            for expense in expenses
        ]

        if insert_data:  # Only run if there are expenses to insert
            # 3. Insert all new records
            query = "INSERT INTO expenses (expense_date, amount, category, notes) VALUES (%s, %s, %s, %s)"
            cursor.executemany(query, insert_data)

        # 4. If everything was successful, commit the transaction
        connection.commit()

    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
        if connection:
            connection.rollback()  # Roll back changes on error
        # Re-raise the exception to be caught by FastAPI
        raise err
    finally:
        if connection and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == "__main__":
    # expenses = fetch_expenses_for_date("2024-08-01")
    # print(expenses)
    # insert_expense("2024-08-25", 30, "Food", "Eat tasty samosa chat")
    # summary = fetch_expense_summary("2024-08-01", "2024-08-05")
    # for record in summary:
    #     print(record)
    expenses = fetch_expenses_for_date("2024-08-03")
    print(expenses)
