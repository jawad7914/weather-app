from flask import Blueprint, request, jsonify
from logic.signup import handle_signup
from logic.login import handle_login
from logic.weatherlogic import get_weather

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

@bp.route('/weather', methods=['GET'])
def weather_route():
    return get_weather()
