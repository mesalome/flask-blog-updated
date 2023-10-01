from flask import current_app
from datetime import datetime, timedelta
from typing import Optional
import jwt

def encode_auth_token(user_id: int) -> str:
    try:
        payload = {
            "exp": datetime.utcnow() + timedelta(days=0, seconds=172800),
            "iat": datetime.utcnow(),
            "sub": user_id,
        }

        return jwt.encode(payload, current_app.config.get("SECRET_KEY"), algorithm="HS256")
    except Exception as e:
        return str(e)

def decode_auth_token(auth_token: str) -> tuple[Optional[str], Optional[str]]:
    try:
        payload = jwt.decode(auth_token, current_app.config.get("SECRET_KEY"), algorithms=["HS256"])
        
        user_id = payload["sub"]
        
        return user_id, None
    except jwt.ExpiredSignatureError:
        return None, "Signature expired"
    except jwt.InvalidTokenError:
        return None, "Invalid token"
    except Exception as e:
        return None, str(e)
