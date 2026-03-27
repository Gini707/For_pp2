from config import *
import psycopg2

def connect():
    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT
        )
        print("CONNECTED SUCCESSFULLY")
        return conn
    except Exception as e:
        print("ERROR:", e)