import bcrypt


def hash_password(password):
    password_bytes = password.encode("utf-8")
    hashed_password = bcrypt.hashpw(password_bytes, bcrypt.gensalt())
    return hashed_password.decode("utf-8")


def verify_password(password, stored_hash):
    try:
        password_bytes = password.encode("utf-8")
        stored_hash_bytes = stored_hash.encode("utf-8")
        return bcrypt.checkpw(password_bytes, stored_hash_bytes)
    except (ValueError, TypeError):
        return False
