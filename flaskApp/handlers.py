from flask import (
    make_response, current_app
)


def get_email_from_token(request,jwt):
    token = request.headers.get('access-token')

    if token is None:
        return None;
    return jwt.decode(token,current_app.config['JWT_SECRET']).get('email')
