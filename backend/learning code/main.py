"""
1. uvicorn server:app --reload
2. uvicorn main:app --reload (when file name is main)
3. what is validating schema?
4. make sure to use GET method instead of POST/PUT/DELETE in postman
"""
from fastapi import FastAPI, HTTPException
from datetime import date
import db_helper_old
from typing import List
from pydantic import BaseModel, ConfigDict

app = FastAPI()

"""
@app.get("/expenses/{expense_date}")
def get_expenses(expense_date: date):
    return f"Received get_expense request {date}"

"""
class Expense(BaseModel):
    #expense_date: date  (this one is omitted because it is not needed in this section)
    amount: float
    category: str
    notes: str

    model_config = ConfigDict(extra="ignore")   #ignores fields not defined

@app.get("/expenses/{expense_date}", response_model=List[Expense])
def get_expenses(expense_date: date):
    expenses = db_helper_old.fetch_expenses_for_date(expense_date)
    #return [Expense(**e) for e in expenses]
    #expenses = [Expense(**row).model_dump() for row in rows]  # enforce model filtering
    return expenses
"""
@app.post("/expenses/{expense_date}")
def add_or_update(expense_date: date, expenses:List[Expense]):
    try:
        db_helper_old.delete_expenses_for_date(expense_date)
        for expense in expenses:
            db_helper_old.insert_expense(expense_date, expense.amount, expense.category, expense.notes)
        return {"message": "Expense updated successfully"}
    except Exception as e:
        # Log the error for debugging purposes
        print(f"An error occurred: {e}")
        # Return a meaningful error message
        raise HTTPException(status_code=500, detail="Failed to update expenses due to a database error.")

db_helper_old.delete_expenses_for_date(expense_date)    #deleting the old list present in frontend
    for expense in expenses:
        db_helper_old.insert_expense(expense_date, expense.amount, expense.category, expense.notes)
    return {"message": "Expense updated successfully"}
"""
#AI response
# In main.py

@app.post("/expenses/{expense_date}")
def add_or_update(expense_date: date, expenses: List[Expense]):
    try:
        # Call the single transactional function
        db_helper_old.add_or_update_expenses_transaction(expense_date, expenses)
        return {"message": "Expenses updated successfully"}
    except Exception as e:
        # Log the specific database error for debugging
        print(f"An error occurred during the transaction: {e}")
        # Return a meaningful error message to the client
        raise HTTPException(status_code=500, detail="Failed to update expenses due to a database error.")


