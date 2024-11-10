from werkzeug.security import generate_password_hash, check_password_hash


def hash_password(pwd:str) -> str:
  return generate_password_hash(pwd)

def check_password(hashed_pwd:str, input_pwd:str) -> bool:
  return check_password_hash(hashed_pwd, input_pwd)
