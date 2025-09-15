import hashlib
import base64

def shorten_session_id(long_string, length=16):
    hash_bytes = hashlib.sha256(long_string.encode('utf-8')).digest()
    short_id = base64.urlsafe_b64encode(hash_bytes).decode('utf-8')
    return short_id.replace('=', '')[:length]

def extract_token_from_header(auth_header: str) -> str:
    if not auth_header or not auth_header["authorization"].startswith("Bearer "):
        return None
    return shorten_session_id(auth_header["authorization"].split(" ")[1])