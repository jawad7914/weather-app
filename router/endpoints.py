from flask import Blueprint, request, jsonify
from logic.signup import handle_signup
from logic.login import handle_login
from logic.weatherlogic import get_weather
from logic.passwords import handle_forgot_password, handle_reset_password
from jwt_token import verify_jwt

bp = Blueprint('routes', __name__)

@bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    response, status = handle_signup(data)
    return jsonify(response), status

@bp.route('/login', methods=['POST'])
def login():
    data = request.json
    response, status = handle_login(data)
    return jsonify(response), status

# Forgot password (send reset token)
@bp.post('/forgot-password')
def forgot_password():
    return jsonify(*handle_forgot_password(request.json))

# Reset password (verify token and update password)
@bp.post('/reset-password')
def reset_password():
    return jsonify(*handle_reset_password(request.json))

from jwt_token import token_required  # import new decorator

@bp.route('/weather', methods=['GET'])
@token_required
def weather_route():
    username = request.user.get("username")  # available from JWT payload
    return get_weather(username)

