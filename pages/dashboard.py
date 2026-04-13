import streamlit as st 
import pandas as pd 
from backend.db import Database
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from css import show_charts

db=Database()
expenses = None


col1,col2,col3,col4= st.columns(4)


with col1 :
    filter = st.pills("Filter",["Monthly","Yearly"])
    if filter=="Monthly" :
        with col3 :
            value = st.text_input("Year and Month(YY-MM)")

    elif filter == "Yearly" :
        with col3 :
            value = st.text_input("Year") 

if filter and value :
    expenses = db.get_expenses(filter,value)           
    show_charts(expenses)





