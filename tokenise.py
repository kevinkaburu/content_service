import jwt
from datetime import datetime, timedelta


def decrypt_token(token,jwt_key):

    try:
        data = jwt.decode(
            token,
            jwt_key,
            algorithms=['HS256']
        )
        return data
    except Exception as e:
        return None