def get_connection():
    try:
        conn = psycopg2.connect(**db_config)
        return conn
    except Exception as e:
        print("Connection error:", e)
        return None