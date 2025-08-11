# login.py
from db.connection import get_connection
from jwt_token import generate_jwt

def handle_login(data):
    if not data:
        return {"error": "No data provided"}, 400

    username = data.get('username')
    password = data.get('password')

    if not all([username, password]):
        return {"error": "Username and password are required"}, 400

    try:
        conn = get_connection()
        if not conn:
            return {"error": "Database connection failed"}, 500

        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s AND password = %s",
                       (username, password))
        user = cursor.fetchone()

        if user:
            # Create token with user info
            payload = {
                "user_id": user[0],
                "username": user[1]
            }
            token = generate_jwt(payload)
            return {"message": f"Login successful! Welcome, {user[1]}!", "token": token}, 200
        else:
            return {"error": "Invalid username or password"}, 401
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
