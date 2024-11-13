from datetime import timedelta
from flask_jwt_extended import create_access_token


def create_token(user_id: int) -> str:
  token_expiration = timedelta(days=1)
  token = create_access_token(identity = user_id, expires_delta = token_expiration)
  
  return token