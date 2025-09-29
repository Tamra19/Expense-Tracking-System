import streamlit as st
from datetime import datetime
import requests

API_URL = "http://localhost:8000"

def add_update_tab():
        selected_date = st.date_input("Enter date:", datetime(2024, 8, 1), label_visibility="collapsed")

        # Format the date to a string to use in the API URL and widget keys
        selected_date_str = selected_date.strftime("%Y-%m-%d")

        # Fetch expenses for the selected date
        response = requests.get(f"{API_URL}/expenses/{selected_date_str}")

        if response.status_code == 200:
            existing_expenses = response.json()
        else:
            st.error("Failed to retrieve expenses")
            existing_expenses = []  # Initialize to empty list on failure

        categories = ["Rent", "Food", "Entertainment", "Shopping", "Other"]
        with st.form(key="expense_form"):
            # Adding sub-headers
            col1, col2, col3 = st.columns(3)
            with col1:
                st.subheader("Amount")
            with col2:
                st.subheader("Category")
            with col3:
                st.subheader("Notes")

            # Adding input fields in a loop
            expenses = []
            for i in range(5):
                if i < len(existing_expenses):
                    # Pre-fill with existing data
                    amount = existing_expenses[i]['amount']
                    category = existing_expenses[i]['category']
                    notes = existing_expenses[i]['notes']
                else:
                    # Default values for new entries
                    amount = 0.0
                    category = "Shopping"
                    notes = ""

                col1, col2, col3 = st.columns(3)

                with col1:
                    # **MODIFIED KEY** to be unique for the selected date
                    amount_input = st.number_input(label="Amount", min_value=0.0, step=1.0, value=amount,
                                                   key=f"amount_{i}_{selected_date_str}", label_visibility="collapsed")
                with col2:
                    # **MODIFIED KEY** to be unique for the selected date
                    category_input = st.selectbox(label="Category", options=categories,
                                                  key=f"category_{i}_{selected_date_str}", index=categories.index(category),
                                                  label_visibility="collapsed")
                with col3:
                    # **MODIFIED KEY** to be unique for the selected date
                    notes_input = st.text_input(label="Notes", value=notes, key=f"notes_{i}_{selected_date_str}",
                                                label_visibility="collapsed")

                expenses.append({
                    'amount': amount_input,
                    'category': category_input,
                    'notes': notes_input
                })

            submit_button = st.form_submit_button()
            if submit_button:
                # Filter out expenses with 0 amount before sending
                filtered_expenses = [expense for expense in expenses if expense['amount'] > 0]

                # Use the formatted date string for the POST request
                post_response = requests.post(f"{API_URL}/expenses/{selected_date_str}", json=filtered_expenses)

                if post_response.status_code == 200:
                    st.success("Expenses updated successfully!")
                else:
                    st.error("Failed to update expenses.")