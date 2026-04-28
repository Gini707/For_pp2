import psycopg2
from config import DB_CONFIG


def get_connection():
    try:
        conn = psycopg2.connect(
            host=DB_CONFIG["host"],
            database=DB_CONFIG["database"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            port=DB_CONFIG["port"]
        )

        conn.set_client_encoding("WIN1251")
        return conn

    except Exception as e:
        print("Connection error:", e)
        return None


def close_connection(conn):
    if conn:
        conn.close()