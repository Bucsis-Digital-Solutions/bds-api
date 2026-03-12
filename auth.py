import bcrypt
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
import os
from dotenv import load_dotenv

load_dotenv()

def hashPassword(password):
    password = password.encode("utf-8")
    salt = bcrypt.gensalt(17)
    hashed = bcrypt.hashpw(password, salt)
    return hashed

def checkPassword(password, hashed):
    return bcrypt.checkpw(password.encode("utf-8"), hashed)

def signToken(data):
    now = datetime.now(timezone.utc)
    claims = {
        "iss": os.getenv("ISSUER_KEY"),
        "iat": now,
        "nbf": now,
        "exp": now + timedelta(minutes=30),
        **data
    }
    token = jwt.encode(claims, os.getenv("PRIVATE_KEY"), algorithm="HS512")
    return token

def decodeToken(token):
    try:
        data = jwt.decode(
            token,
            os.getenv("PRIVATE_KEY"),
            algorithms=["HS512"],
            issuer=os.getenv("ISSUER_KEY")
        )
        return data
    except JWTError as e:
        print(f"Token validation error: {e}")
        return None