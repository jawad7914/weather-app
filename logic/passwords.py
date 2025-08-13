from jwt_token import generate_jwt, verify_jwt
from db.connection import get_connection
import datetime

# Forgot password handler
def handle_forgot_password(data):
    email = data.get("email")
    if not email:
        return {"error": "Email required"}, 400

    # Normally: verify email exists in DB
    payload = {
        "email": email,
        "type": "reset_password",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=12)  # short expiry
    }
    token = generate_jwt(payload)
    
    # Placeholder for sending email
    print(f"Password reset link: http://yourapp/reset-password?token={token}")

    return {"message": "Password reset link sent to your email"}, 200

# Reset password handler
def handle_reset_password(data):
    token = data.get("token")
    new_password = data.get("new_password")
    if not token or not new_password:
        return {"error": "Token and new password required"}, 400

    decoded = verify_jwt(token)
    if not decoded or decoded.get("type") != "reset_password":
        return {"error": "Invalid or expired token"}, 400

    email = decoded["email"]

    # Update password in DB
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("UPDATE users SET password = %s WHERE email = %s", (new_password, email))
    conn.commit()
    cur.close()
    conn.close()

    return {"message": "Password updated successfully"}, 200
