import streamlit as st 
from backend.db import Database
db = Database()
from css import css_add_expense

css_add_expense()



name_db = db.get_users()[["user_id", "name"]]
cat_db = db.get_categories()[["cat_id", "title"]]

user_map = dict(zip(name_db["name"], name_db["user_id"]))
cat_map = dict(zip(cat_db["title"], cat_db["cat_id"]))

names = list(user_map.keys())
categories = list(cat_map.keys())

_, center, _ = st.columns([1, 2, 1])

with center : 

    with st.form(key="key1",clear_on_submit=True,width=600,height=540):
        st.subheader("Add Expenses")
        col1,col2,col3 = st.columns(3)
        with col1 :
            name = st.selectbox("User ",names)
        with col2 :    
            category = st.selectbox("Category ",categories)
        with col3 :    
            amount = st.number_input("Amount ",min_value=0)
        note = st.text_input("Any Notes  ")
        date = str(st.date_input("Date  "))
        button1=st.form_submit_button("Add Expense")

    if button1 : 
        cat_id = cat_map[category]
        user_id = user_map[name]
        try :
            db.add_expense(cat_id,user_id,amount,note,date)
            st.success("Expense Added Successfully!")
        except Exception as e : 
            st.error(e)    
            st.warning("Error Ocuured while adding expense.")
