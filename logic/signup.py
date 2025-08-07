from db.connection import get_connection

def handle_signup(data):
    if not data:
        return {"error": "No data provided"}, 400

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not all([username, email, password]):
        return {"error": "Username, email, and password are required"}, 400

    try:
        conn = get_connection()
        if not conn:
            return {"error": "Database connection failed"}, 500

        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
                       (username, email, password))
        conn.commit()
        return {"message": "Signup successful"}, 200
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()

