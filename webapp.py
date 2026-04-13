import streamlit as st 
from css import css_webapp

# PAGE CONFIGURATION SETUP
st.set_page_config(
    page_title="ExpenseManager",
    page_icon="💸",
    layout="wide"
) 
css_webapp()


# PAGES 

details = st.Page(
    page="pages/details.py",
    title="Details",
    icon="📗"

)


addExpense = st.Page(
    page='pages/add_expense.py',
    icon='➕',
    title='Add Expenses'
)
dashBoard = st.Page(
    page='pages/dashboard.py',
    icon='📊',
    title='Dashboard'
)
developerInfo = st.Page(
    page='pages/developer_info.py',
    icon='👨‍💻',
    title="Developer Info"
)
configurationPage = st.Page(
    page="pages/configuration.py",
    icon="📲",
    title="Configuration"
)


# NAVIGATION 
nav = st.navigation(
    {
        "User":[details],
        "Tools":[addExpense,dashBoard,configurationPage],
        "Info":[developerInfo]
    }
)

# RUN THE NAVIGATION BAR 
nav.run()

# TAGS ON SIDEBAR IN ALL PAGES 
st.sidebar.write("Made with 💌 by Shivam")