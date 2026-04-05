import mysql.connector

def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",          # Change if your username is different
        password="",  # <--- CHANGE THIS TO YOUR MYSQL PASSWORD
        database="billing_system"
    )
