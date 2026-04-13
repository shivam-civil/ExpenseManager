import pandas as pd
import sqlite3
from backend.sheets import SheetDB  
import gspread 
"""
DATABASE STRUCTURE : 
> THREE TABLES : Users , Category , Expenses 
1) Users table contains user_id,name,reation,added_date
2) Category table contains cat_id and title 
3) Expenses table contains exp_id , cat_id(foreign key), user_id(foreign_key) and note
Note : To avoid expenses category stored multiple times repitative in expenses table whihc cause memory increase dude to string store, we are gong to store the cat_id in Expenses table. cat_id will take less space than strings.
"""

class Database:
    
    def __init__(self):
        self.__conn = sqlite3.connect("backend/expenses.db", check_same_thread=False)
        self.__cur = self.conn.cursor()
        self.conn.execute("PRAGMA foreign_keys = ON;")
        self.sheet = None

    @property    
    def conn(self):
        return self.__conn 
       
    @property
    def cur(self):
        return self.__cur
    
    def create_db(self):

        # CREATE Users TABLE 
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT ,
        name TEXT NOT NULL ,
        relation TEXT NOT NULL,
        added_date DATE NOT NULL,
        is_active INTEGER DEFAULT 1
        )
        """)
        self.conn.commit()

        # CREATE Category TABLE 
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS Category(
        cat_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL
        )
        """)
        self.conn.commit()

        # CREATE Expenses TABLE 
        self.conn.execute("""
        CREATE TABLE IF NOT EXISTS Expenses(
        exp_id INTEGER PRIMARY KEY AUTOINCREMENT,
        cat_id INTEGER ,
        user_id INTEGER,
        note TEXT,
        amount REAL ,
        date TEXT ,

        FOREIGN KEY (cat_id) REFERENCES Category(cat_id),
        FOREIGN KEY (user_id) REFERENCES Users(user_id)                  
        )
        """)
        self.conn.commit()



    def drop_db(self):
        self.cur.execute("DROP TABLE IF EXISTS Expenses")
        self.cur.execute("DROP TABLE IF EXISTS Category")
        self.cur.execute("DROP TABLE IF EXISTS Users")
        self.conn.commit()

    def add_expense(self,cat_id,user_id,amount,note,date):

        if self.sheet is None :
            from backend.sheets import SheetDB
            self.sheet = SheetDB()
        # SQLITE INSERT
        self.cur.execute("""
        INSERT INTO Expenses(cat_id,user_id,amount,note,date)
        VALUES (?,?,?,?,?)
        """,(cat_id,user_id,amount,note,date))
        self.conn.commit()

        # GOOGLE SHEETS APPEND

        # 1) FETCH NAMES FOR SHEETS
        self.cur.execute("SELECT name FROM Users WHERE user_id = ?",(user_id,))
        user_name = self.cur.fetchone()[0]

        self.cur.execute("SELECT title FROM Category WHERE cat_id = ?",(cat_id,))
        category_name = self.cur.fetchone()[0]

        # 2) APPEND TO SHEETS 
        self.sheet.append_row([
            user_name,
            category_name,
            amount,
            date,
            note
        ])



    def add_category(self,title):
        self.cur.execute("""
        INSERT INTO Category(title)
        VALUES (?)
        """,(title,))
        self.conn.commit()


    def add_user(self,name,relation,added_date):
        self.cur.execute("""
        INSERT INTO Users(name,relation,added_date)
        VALUES (?,?,?)
        """,(name,relation,added_date))
        self.conn.commit()

    def remove_user(self,user_id):   # SOFT DELETE
        self.cur.execute("""
        UPDATE Users
        SET is_active = 0 
        WHERE user_id = ?
        """,(user_id,))
        self.conn.commit()

    def get_expenses(self,filter_type=None,value=None):
        query="""
        SELECT 
        Expenses.exp_id as exp_id,
        Users.name as name,
        Category.title as category,
        Expenses.amount as amount,
        Expenses.date as date,
        Expenses.note as note
        FROM Expenses 
        JOIN Users ON Expenses.user_id = Users.user_id
        JOIN Category ON Expenses.cat_id = Category.cat_id  
        """
        params =[]
        if filter_type =="monthly":
            query += " WHERE strftime('%Y-%m',Expenses.date) = ? "
            params.append(value)
        elif filter_type =="yearly" :
            query += " WHERE strftime('%Y',Expenses.date) = ? "
            params.append(value)
        
        self.cur.execute(query,params)
        result = self.cur.fetchall()
        columns = [col[0] for col in self.cur.description]
        return pd.DataFrame(result,columns=columns)

    def get_users(self):
        query ="SELECT user_id,name,relation,added_date,is_active FROM Users"
        df = pd.read_sql_query(query,self.conn)
        return df 

    def get_categories(self):
        query = "SELECT cat_id, title FROM  Category"
        df = pd.read_sql_query(query,self.conn)
        return df
    
    def close(self):
        self.conn.close()


