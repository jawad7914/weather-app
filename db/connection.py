import psycopg2

def get_connection():
    try:
        conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="1234",
            port=5432
        )
        print("Connection to PostgreSQL successful!")
        return conn
    except psycopg2.Error as e:
        print(f"Error: {e}") 
        return None
    
