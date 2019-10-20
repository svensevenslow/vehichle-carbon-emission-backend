import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, make_response, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskApp.db import connection
import jwt

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=['POST'])
def register_user():
    req_data = request.get_json();
    email = req_data['email']
    name = req_data['name']
    password = generate_password_hash(req_data['password'])
    contact = req_data['contact']
    mysql_insert_query = """INSERT INTO user (name, email, password, contact) 
                                    VALUES (%s, %s, %s, %b) """
    record_tuple = (name,email,password,contact)
    mysql_check_existing_user_query = """Select * from user where email = (%s)"""
    check_existing_user_tuple = [email]
    try:
        c, conn = connection()
        existing_user = c.execute(mysql_check_existing_user_query,check_existing_user_tuple);

        if existing_user > 0:
            return make_response({"message": "user already exists, please login"},400)

        c.execute(mysql_insert_query, record_tuple)
        conn.commit()
        c.close()
        conn.close()

        token_payload = {"email": email}
        jwt_token = jwt.encode(token_payload, current_app.config['JWT_SECRET'],algorithm='HS256')

        return make_response({"message":"Registration successful", "token":jwt_token.decode('utf8')},200)

    except Exception as e:
        return str(e)


@bp.route('/loginWithToken', methods=['GET'])
def login_with_token():
    token = request.headers.get('access-token')

    if token is None:
        return make_response({"message":"access-token not sent"},401)

    try:
        payload = jwt.decode(token,current_app.config['JWT_SECRET'])
    except jwt.exceptions.InvalidTokenError as e:
        return make_response({"message": "Invalid token error, login failed"},401)

    return make_response({"message":"successful login"}, 200)


# @bp.route('/loginWithCredentials', methods=['POST'])
# def login_with_credentials():
#     req_data = request.get_json()
#     email = req_data.get('email')
#     password = req_data.get('password')
#     mysql_check_user_query = """"Select"""
