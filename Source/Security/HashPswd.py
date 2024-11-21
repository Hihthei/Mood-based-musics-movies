import bcrypt

def hash_pswd(pswd: str) -> str:
    salt = b'$2b$12$NY/kWGwrf88yHHhVshtyv.'
    return bcrypt.hashpw(pswd.encode('utf-8'), salt).decode('utf-8')
