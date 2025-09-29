"""
1. command to run the program: streamlit run .\file_name.py
2. iterative development- you write one part of code and then you run it to see if its working or not and repeat the process until the code is complete.
-> Streamlit is an open-source python library that allows developers to create beautiful, interactive
    web applications for machine learning and data analysis with minimal effort.
-> Creating a web application with streamlit involves writing standard python scripts, where you define
    the layout and interactivity of the app using streamlit's rich set of widgets and functions
-> streamlit automatically handles the frontend and updates the UI based on user interactions, making it
    straightforward to prototype and deploy data-driven applications.
-> the framework supports hot-reloading, which means changes to the code are immediately reflected in the
    app without needing to restart the server, enhancing the development process.

"""
import streamlit as st
import pandas as pd

st.title("Expense Management System")

"""
expense_dt = st.date_input("Expense Date: ")
if expense_dt:
    st.write(f"Fetching expenses for {expense_dt}")

"""

#Text Elements
st.header("Streamlit Core Features")
st.subheader("Text Elements")
st.text("This is a simple text element.")

#Data display
st.subheader("Data Display")
st.write("1. Here is a simple table:")
st.table({"Column1": [1,2,3], "Column2": [4,5,6]})

st.write("2. Here is a table made using pandas")
df = pd.DataFrame({
    "Date": ["2024-08-01", "2024-08-02", "2024-08-03"],
    "Amount": [250,134,340]
})

st.table(df)

#Charts
st.subheader("Charts")
st.line_chart([1,2,3,4])

#User Input
st.subheader("User input")
value = st.slider("Select a value", 0,100)
st.write(f"Selected value: {value}")

#Interactive Widgets Example
st.title("Interactive Widgets Examples")

#Checkbox
if st.checkbox("Show/Hide"):
    st.write("Checkbox is checked")

#Selectbox
option = st.selectbox("Select a number", [1,2,3,4,5])
st.write(f"You selected {option}")

option = st.selectbox("Category", ["Food", "Rent", "Shopping", "Entertainment"], label_visibility="collapsed")
st.write(f"You selected {option}")

#Multiselect
options = st.multiselect("Select multiple numbers", [1,2,3,4,5,6,7,8,9])
st.write(f"You selected {options}")

"""
app.py that is taught in class (with errors)
import streamlit as st
from datetime import datetime
import requests

API_URL = "http://localhost:8000"

st.title("Expense Tracking System")

tab1, tab2 = st.tabs(["Add/Update", "Analytics"])

with tab1:
    selected_date = st.date_input("Enter date:", datetime(2024, 8, 1), label_visibility="collapsed")

    # Format the date to a string ONCE
    selected_date_str = selected_date.strftime("%Y-%m-%d")

    # Make only ONE GET request with the formatted string
    response = requests.get(f"{API_URL}/expenses/{selected_date_str}")

    if response.status_code == 200:
        existing_expenses = response.json()
    else:
        st.error("Failed to retrieve expenses")
        existing_expenses = []

    categories = ["Rent", "Food", "Entertainment", "Shopping", "Other"]
    with st.form(key="expense_form"):    #key is used to uniquely identify forms
        #adding sub-headers
        col1,col2,col3 =st.columns(3)
        with col1:
            st.subheader("Amount")
        with col2:
            st.subheader("Category")
        with col3:
            st.subheader("Notes")

        #adding columns thru for loop
        expenses = []
        for i in range(5):
            if i < len(existing_expenses):
                amount = existing_expenses[i]['amount']
                category = existing_expenses[i]['category']
                notes = existing_expenses[i]['notes']
            else:
                #default values
                amount = 0.0
                category = "Shopping"
                notes = ""

            col1, col2, col3 = st.columns(3)

            with col1:
                amount_input = st.number_input(label="Amount", min_value=0.0, step=1.0, value=amount, key=f"amount_{i}", label_visibility="collapsed")
            with col2:
                category_input = st.selectbox(label="Category", options=categories, key=f"category_{i}", index=categories.index(category), label_visibility="collapsed")
            with col3:
                notes_input = st.text_input(label="Notes", value=notes, key=f"notes_{i}", label_visibility="collapsed")

            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })
        submit_button = st.form_submit_button()
        if submit_button:
            filtered_expenses = [expense for expense in expenses if expense['amount']>0]

            response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)
            if response.status_code == 200:
                st.success("Expenses updated successfully!")
            else:
                st.error("Failed to update expenses.")




"""

"""
import streamlit as st
from datetime import datetime
import requests

API_URL = "http://localhost:8000"

st.title("Expense Tracking System")

tab1, tab2 = st.tabs(["Add/Update", "Analytics"])

with tab1:
    selected_date = st.date_input("Enter date:", datetime(2024, 8, 1), label_visibility="collapsed")

    # Format the date to a string ONCE
    selected_date_str = selected_date.strftime("%Y-%m-%d")

    # ADD THIS LINE FOR DEBUGGING
    st.write(f"DEBUG: Requesting data for date: {selected_date_str}")

    # Make only ONE GET request with the formatted string
    response = requests.get(f"{API_URL}/expenses/{selected_date_str}")

    if response.status_code == 200:
        existing_expenses = response.json()
    else:
        st.error("Failed to retrieve expenses")
        existing_expenses = []

    categories = ["Rent", "Food", "Entertainment", "Shopping", "Other"]
    with st.form(key="expense_form"):    #key is used to uniquely identify forms
        #adding sub-headers
        col1,col2,col3 =st.columns(3)
        with col1:
            st.subheader("Amount")
        with col2:
            st.subheader("Category")
        with col3:
            st.subheader("Notes")

        #adding columns thru for loop
        expenses = []
        for i in range(5):
            if i < len(existing_expenses):
                amount = existing_expenses[i]['amount']
                category = existing_expenses[i]['category']
                notes = existing_expenses[i]['notes']
            else:
                #default values
                amount = 0.0
                category = "Shopping"
                notes = ""

            col1, col2, col3 = st.columns(3)

            with col1:
                amount_input = st.number_input(label="Amount", min_value=0.0, step=1.0, value=amount, key=f"amount_{i}", label_visibility="collapsed")
            with col2:
                category_input = st.selectbox(label="Category", options=categories, key=f"category_{i}", index=categories.index(category), label_visibility="collapsed")
            with col3:
                notes_input = st.text_input(label="Notes", value=notes, key=f"notes_{i}", label_visibility="collapsed")

            expenses.append({
                'amount': amount_input,
                'category': category_input,
                'notes': notes_input
            })
        submit_button = st.form_submit_button()
        if submit_button:
            filtered_expenses = [expense for expense in expenses if expense['amount']>0]

            response = requests.post(f"{API_URL}/expenses/{selected_date}", json=filtered_expenses)
            if response.status_code == 200:
                st.success("Expenses updated successfully!")
            else:
                st.error("Failed to update expenses.")




"""