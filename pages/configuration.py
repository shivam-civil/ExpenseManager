import streamlit as st 
from backend.db import Database

db = Database()

tab1,tab2,tab3 = st.tabs(["User Settings","Category Settings","Database Controls"])

with tab3:

    st.subheader("Database Settings")
    col1,col2 = st.columns(2)
    with col1 :
        create_button =st.button("Create Database")
    with col2 :
        drop_button = st.button("Drop Database")

    if create_button :
        try :
            db.create_db()
            st.success("Database Created!")
        except Exception as e1 :
            st.error(e1)
            st.warning("Error Occured while creating database")

    if drop_button : 
        try :
            db.drop_db()
            st.success("Database Dropped!")  
        except Exception as e2 :
            st.error(e2)
            st.warning("Error Occured while droping database.")

with tab1 : 
    with st.expander("Add User "):
        with st.form("key1",clear_on_submit=True,width=600,height=300):
            st.subheader("Add User")
            coln1,coln2 = st.columns(2)
            with coln1 : 
                name = st.text_input("Name : ")
            with coln2 :
                relation = st.text_input("Relation : ")
            added_date = st.date_input("Date : ") 
            button1=st.form_submit_button("Add User") 
        if button1 : 
            try : 
                db.add_user(name,relation,added_date)
                st.success("User Added!")
            except Exception as e3 :
                st.error(e3)   
                st.warning("Error Occured while adding user.") 

    with st.expander("Remove User "):
        with st.form("key2",clear_on_submit=True,width=600,height=220) :
            st.subheader("Remove User ")
            user_id = st.number_input("User Id : ",min_value=0)
            button2 = st.form_submit_button("Remove")
        if button2 :
            try :
                db.remove_user(user_id)
                st.success("User Removed!")
            except Exception as e4 :
                st.error(e4)
                st.warning("Error Occured while removing user.")   


with tab2 :
    with st.expander("Add Category"):
        with st.form("key3",clear_on_submit=True,width=600,height=220):
            st.subheader("Add Category")
            title = st.text_input("Category Name : ")    
            button3=st.form_submit_button("Add Category")
        if button3 : 
            try : 
                db.add_category(title)
                st.success("Category Added!")
            except Exception as e5 :
                st.error(e5)
                st.warning("Error Occured while adding category")                
 
    
                
                
        