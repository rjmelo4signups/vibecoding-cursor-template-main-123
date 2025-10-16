import streamlit as st
import pandas as pd
from datetime import datetime
from google_sheets_helper import append_expense_to_sheet, setup_sheet_headers, load_expenses_from_sheet, clear_all_expenses_from_sheet, delete_expense_from_sheet
from voice_parser import parse_expense_with_gemini, get_voice_input_examples
# Audio recording will be added in future versions

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

# Voice input section
st.sidebar.subheader("🎤 AI-Powered Input")
st.sidebar.markdown("Describe your expense naturally:")

# Text-based voice input (works immediately)
voice_text_input = st.sidebar.text_input(
    "Describe your expense:", 
    placeholder="e.g., 'I spent 15 euros on lunch at the cafeteria'",
    key="voice_input",
    on_change=None
)

# Process text-based voice input when button is clicked
if voice_text_input and st.sidebar.button("🤖 Parse with Gemini"):
    with st.spinner("Parsing with Gemini..."):
        parsed_expense = parse_expense_with_gemini(voice_text_input)
        
        if parsed_expense:
            st.sidebar.success("✅ Parsed successfully!")
            st.sidebar.json(parsed_expense)
            
            # Automatically add the expense to the list
            new_expense = {
                "Date": datetime.now().strftime("%Y-%m-%d"),
                "Item": parsed_expense['item'],
                "Amount": parsed_expense['amount'],
                "Category": parsed_expense['category'],
                # Hidden unique key for precise deletes in Google Sheets
                "Timestamp": datetime.now().isoformat(timespec='milliseconds')
            }
            
            # Add to expenses list
            st.session_state.expenses.append(new_expense)
            
            # Try to save to Google Sheets if configured
            if SPREADSHEET_ID != "your-spreadsheet-id-here":
                try:
                    # Setup headers if needed
                    setup_sheet_headers(SPREADSHEET_ID)
                    
                    # Append to Google Sheet
                    success, message = append_expense_to_sheet(SPREADSHEET_ID, new_expense)
                    if success:
                        st.sidebar.success(f"✅ Added {parsed_expense['item']} for €{parsed_expense['amount']:.2f} and saved to Google Sheets!")
                    else:
                        st.sidebar.warning(f"⚠️ Added {parsed_expense['item']} for €{parsed_expense['amount']:.2f} (Google Sheets: {message})")
                except Exception as e:
                    st.sidebar.warning(f"⚠️ Added {parsed_expense['item']} for €{parsed_expense['amount']:.2f} (Google Sheets error: {str(e)})")
            else:
                st.sidebar.success(f"✅ Added {parsed_expense['item']} for €{parsed_expense['amount']:.2f}!")
            
            # Clear the input field
            st.rerun()
        else:
            st.sidebar.error("❌ Could not parse the expense. Please try again or use manual input.")


# Voice input examples
with st.sidebar.expander("💡 Voice Examples"):
    st.markdown("Try saying things like:")
    examples = get_voice_input_examples()
    for example in examples[:4]:  # Show first 4 examples
        st.markdown(f"• \"{example}\"")

st.sidebar.markdown("---")

# Manual input fields
st.sidebar.subheader("✏️ Manual Input")
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
            "Category": expense_category,
            # Hidden unique key for precise deletes in Google Sheets
            "Timestamp": datetime.now().isoformat(timespec='milliseconds')
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
    
    # Display expenses table with delete buttons
    st.subheader("📋 Your Expenses")
    
    # Create header row
    header_col1, header_col2, header_col3, header_col4, header_col5 = st.columns([2, 1, 1, 1, 1])
    with header_col1:
        st.markdown("**Item**")
    with header_col2:
        st.markdown("**Amount**")
    with header_col3:
        st.markdown("**Category**")
    with header_col4:
        st.markdown("**Date**")
    with header_col5:
        st.markdown("**Action**")
    
    # Add a subtle divider
    st.markdown("---")
    
    # Create a custom display with delete buttons
    for i, expense in enumerate(st.session_state.expenses):
        col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 1])
        
        with col1:
            st.write(f"📦 {expense['Item']}")
        with col2:
            st.write(f"💰 €{expense['Amount']:.2f}")
        with col3:
            # Add category emoji for better visual appeal
            category_emojis = {
                "Groceries": "🛒",
                "Restaurants": "🍽️", 
                "Cafeteria": "☕",
                "Transportation": "🚌",
                "Entertainment": "🎬",
                "Shopping": "🛍️",
                "Bills": "📄",
                "Donations": "❤️",
                "Other": "📝"
            }
            emoji = category_emojis.get(expense['Category'], "📝")
            st.write(f"{emoji} {expense['Category']}")
        with col4:
            st.write(f"📅 {expense['Date']}")
        with col5:
            if st.button("🗑️", key=f"delete_{i}", help="Delete this expense", type="secondary"):
                # Delete from local list
                del st.session_state.expenses[i]
                
                # Delete from Google Sheets if configured
                if SPREADSHEET_ID != "your-spreadsheet-id-here":
                    try:
                        success, message = delete_expense_from_sheet(SPREADSHEET_ID, expense)
                        if success:
                            st.success(f"✅ Deleted {expense['Item']} from both app and Google Sheets!")
                        else:
                            st.warning(f"⚠️ Deleted from app, but Google Sheets error: {message}")
                    except Exception as e:
                        st.warning(f"⚠️ Deleted from app, but Google Sheets error: {str(e)}")
                else:
                    st.success(f"✅ Deleted {expense['Item']} from app!")
                
                st.rerun()
        
        # Add a subtle separator between rows
        if i < len(st.session_state.expenses) - 1:
            st.markdown("---")
    
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
