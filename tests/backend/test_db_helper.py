"""
1. in big projects there are 2 different databases, one for testing and one actual db
2. you can find the directory of a file by typing print(__file__)
3. better method- print(os.path.dirname(__file__))
4. how to connect the main directory for testing
    project_root = os.path.join(os.path.dirname(__file__), '..')
    sys.path.insert(0, project_root)
5. HOMEWORK: write test cases for all the functions in the db_helper.py file
6. in production, you do testing by failing the tests first, then passing them and iterating the same process
7. breakdown of project is an important task.
"""
from backend import db_helper_old

def test_fetch_expenses_for_date():
    expenses = db_helper_old.fetch_expenses_for_date("2024-08-15")

    assert len(expenses) == 1
    assert expenses[0]["amount"] == 10
    assert expenses[0]["category"] == "Shopping"
    assert expenses[0]["notes"] == "Bought potatoes"

def test_fetch_expenses_for_invalid_date():
    expenses = db_helper_old.fetch_expenses_for_date("9999-08-15")

    assert len(expenses) == 0

def test_fetch_expense_summary_invalid_range():
    summary = db_helper_old.fetch_expense_summary("9999-08-01", "9999-08-05")
    assert len(summary) == 0