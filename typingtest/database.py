from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()
conn = None

# I read online it's better to export the connection object rather than the cursor object, hence will be exporting connection object and creating a new cursor at any place i need it
def get_connection():
    global conn

    if conn is None or not conn.is_connected():
        try:
            conn = mysql.connector.connect(
                host = "localhost",
                port = 3306,
                user = "root",
                password = os.getenv("mysql_root_password"),
                use_pure = True,
            )

            cursor_ = conn.cursor()
            cursor_.execute("CREATE DATABASE IF NOT EXISTS mountracer__db_123;")

            cursor_.close()
            conn.close()

            conn = mysql.connector.connect(
                host = "localhost",
                port = 3306,
                user = "root",
                password = os.getenv("mysql_root_password"),
                use_pure = True,
                database = "mountracer__db_123"
            )

        except Exception as e:
            print("Error: " + str(e))
        
        if conn.is_connected(): print("database is now connected!")

    return conn

def check_for_table(type: str):
    pass

# def get_connection():
#     global conn

#     if conn is None or not conn.is_connected():
#         try: 
#             conn = mysql.connector.connect(
#                 host = "localhost",
#                 port = 3306,
#                 user = "root",
#                 password = os.getenv("mysql_root_password"),
#                 use_pure = True,
#                 database = "mountracer__db_123"
#             )
#         except:
#             print("mountracer__db_123 does not exist, creating a new database")

#             conn_ = mysql.connector.connect(
#                 host = "localhost",
#                 port = 3306,
#                 user = "root",
#                 password = os.getenv("mysql_root_password"),
#                 use_pure = True,
#             )

#             conn_.cursor().execute("CREATE DATABASE IF NOT EXISTS mountracer__db_123;")
#             conn_.close()

#             conn = mysql.connector.connect(
#                 host = "localhost",
#                 port = 3306,
#                 user = "root",
#                 password = os.getenv("mysql_root_password"),
#                 use_pure = True,
#                 database = "mountracer__db_123"
#             )
            


#         if conn.is_connected(): print("Connection with database has been established!")
#     else: print("Connection with MySQL database already exists")

#     return conn