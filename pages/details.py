import streamlit as st 
from backend.db import Database
import pandas as pd 


db = Database()

users = db.get_users()
categories = db.get_categories()

with st.expander(label="View Users"):
    st.dataframe(users)
    pass

with st.expander(label="View Categories"):
    st.dataframe(categories)
    pass