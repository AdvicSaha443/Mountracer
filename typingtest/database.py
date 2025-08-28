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