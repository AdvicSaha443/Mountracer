from dotenv import load_dotenv
import mysql.connector
import os

conn = None
load_dotenv()

def get_connection():
    global conn

    if conn is None or not conn.is_connected():
        conn = mysql.connector.connect(
            host = "localhost",
            port = 3306,
            user = "root",
            password = os.getenv("mysql_root_password"),
            use_pure = True
        )

    return conn

# try:
#     conn = mysql.connector.connect(
#         host="127.0.0.1",
#         port=3306,
#         user="root",
#         password="Advicsaha@443@443_443"  # hardcode temporarily to rule out .env issue
#     )
#     print("Connected?", conn.is_connected())
# except Exception as e:
#     print("Error:", e)
#     traceback.print_exc()
