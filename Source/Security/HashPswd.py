import bcrypt

def hash_pswd(pswd: str) -> str:
    hashed = bcrypt.hashpw(pswd.encode('utf-8'), bcrypt.gensalt())
    return hashed.decode('utf-8')

def verify_pswd(pswd: str, hashed_pswd: str) -> bool:
    return bcrypt.checkpw(pswd.encode('utf-8'), hashed_pswd.encode('utf-8'))
