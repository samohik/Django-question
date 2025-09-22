import datetime
import jwt


def create_jwt(user):
    payload = {
        "id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1),
        "iat": datetime.datetime.utcnow(),
    }

    token = jwt.encode(payload, 'SECRET', algorithm="HS256")
    return token


def decode_jwt(token):
    return jwt.decode(token, 'SECRET', algorithms=["HS256", ])