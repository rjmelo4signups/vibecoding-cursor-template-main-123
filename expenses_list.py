import streamlit as st
import pandas as pd
from datetime import datetime
from google_sheets_helper import append_expense_to_sheet, setup_sheet_headers, load_expenses_from_sheet, clear_all_expenses_from_sheet

# Set page title
st.title("💰 Expenses List")

# Initialize session state to store expenses
if 'expenses' not in st.session_state:
    st.session_state.expenses = []

# Google Sheets configuration
SPREADSHEET_ID = st.secrets.get("GOOGLE_SHEET_ID", "your-spreadsheet-id-here")

# Load existing expenses from Google Sheets on startup
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = True
    
    if SPREADSHEET_ID != "your-spreadsheet-id-here":
        with st.spinner("Loading expenses from Google Sheets..."):
            try:
                success, expenses_data = load_expenses_from_sheet(SPREADSHEET_ID)
                if success:
                    st.session_state.expenses = expenses_data
                    st.success(f"Loaded {len(expenses_data)} expenses from Google Sheets!")
                else:
                    st.warning(f"Could not load from Google Sheets: {expenses_data}")
            except Exception as e:
                st.warning(f"Error loading from Google Sheets: {str(e)}")
    else:
        st.info("Google Sheets not configured. Add your spreadsheet ID to load existing data.")

# Sidebar for adding new expenses
st.sidebar.header("Add New Expense")

# Input fields for new expense
expense_name = st.sidebar.text_input("What did you buy?")
expense_amount = st.sidebar.number_input("How much did it cost?", min_value=0.0, step=0.01, format="%.2f")
expense_category = st.sidebar.selectbox("Category", ["Groceries", "Restaurants", "Cafeteria", "Transportation", "Entertainment", "Shopping", "Bills", "Donations", "Other"])

# Add expense button
if st.sidebar.button("Add Expense"):
    if expense_name and expense_amount > 0:
        # Create new expense entry
        new_expense = {
            "Date": datetime.now().strftime("%Y-%m-%d"),
            "Item": expense_name,
            "Amount": expense_amount,
            "Category": expense_category
        }
        
        # Add to expenses list
        st.session_state.expenses.append(new_expense)
        
        # Try to save to Google Sheets
        if SPREADSHEET_ID != "your-spreadsheet-id-here":
            try:
                # Setup headers if needed
                setup_sheet_headers(SPREADSHEET_ID)
                
                # Append to Google Sheet
                success, message = append_expense_to_sheet(SPREADSHEET_ID, new_expense)
                if success:
                    st.sidebar.success(f"Added {expense_name} for €{expense_amount:.2f} and saved to Google Sheets!")
                else:
                    st.sidebar.warning(f"Added {expense_name} for €{expense_amount:.2f} (Google Sheets: {message})")
            except Exception as e:
                st.sidebar.warning(f"Added {expense_name} for €{expense_amount:.2f} (Google Sheets error: {str(e)})")
        else:
            st.sidebar.success(f"Added {expense_name} for €{expense_amount:.2f}")
    else:
        st.sidebar.error("Please fill in both name and amount!")

# Main content area
st.header("Your Expenses")

if st.session_state.expenses:
    # Convert to DataFrame for better display
    df = pd.DataFrame(st.session_state.expenses)
    
    # Display expenses table
    st.dataframe(df, use_container_width=True)
    
    # Calculate and display total
    total_spent = df['Amount'].sum()
    st.metric("Total Spent", f"€{total_spent:.2f}")
    
    # Show expenses by category
    st.subheader("Expenses by Category")
    category_totals = df.groupby('Category')['Amount'].sum().sort_values(ascending=False)
    
    # Create a colorful bar chart
    import plotly.express as px
    
    # Convert to DataFrame for plotly
    category_df = category_totals.reset_index()
    category_df.columns = ['Category', 'Amount']
    
    # Create bar chart with different colors
    fig = px.bar(
        category_df, 
        x='Category', 
        y='Amount',
        title="Expenses by Category",
        color='Category',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    # Update layout for better appearance
    fig.update_layout(
        showlegend=False,
        xaxis_title="Category",
        yaxis_title="Amount (€)",
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Clear all expenses button with confirmation
    if st.button("🗑️ Clear All Expenses", type="secondary"):
        st.session_state.show_clear_confirmation = True
    
    # Show confirmation dialog if needed
    if st.session_state.get('show_clear_confirmation', False):
        st.warning("⚠️ This will delete ALL expenses from both the app and Google Sheets!")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("✅ Yes, Delete All", type="primary"):
                # Clear local expenses
                st.session_state.expenses = []
                
                # Clear Google Sheets if configured
                if SPREADSHEET_ID != "your-spreadsheet-id-here":
                    try:
                        success, message = clear_all_expenses_from_sheet(SPREADSHEET_ID)
                        if success:
                            st.success("✅ All expenses cleared from both app and Google Sheets!")
                        else:
                            st.warning(f"⚠️ Cleared from app, but Google Sheets error: {message}")
                    except Exception as e:
                        st.warning(f"⚠️ Cleared from app, but Google Sheets error: {str(e)}")
                else:
                    st.success("✅ All expenses cleared from app!")
                
                # Reset confirmation state
                st.session_state.show_clear_confirmation = False
                st.rerun()
        
        with col2:
            if st.button("❌ Cancel"):
                st.session_state.show_clear_confirmation = False
                st.info("Clear operation cancelled.")
                st.rerun()
        
else:
    st.info("No expenses added yet. Use the sidebar to add your first expense!")

# Instructions
st.markdown("---")
st.markdown("### How to use this app:")
st.markdown("1. Fill in the form on the left sidebar")
st.markdown("2. Click 'Add Expense' to save it")
st.markdown("3. View your expenses and spending summary below")
st.markdown("4. Use 'Clear All Expenses' to start over")
