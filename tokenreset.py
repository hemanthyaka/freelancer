from itsdangerous import URLSafeTimedSerializer
from key import secret_key,salt,salt2
def token(data,salt):
    serializer=URLSafeTimedSerializer(secret_key)
    return serializer.dumps(data,salt=salt)