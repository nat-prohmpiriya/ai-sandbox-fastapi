from typing import Any, Dict
from firebase_admin import auth, credentials, initialize_app
from firebase_admin.auth import InvalidIdTokenError, ExpiredIdTokenError

cred: credentials.Certificate = credentials.Certificate("src/config/firebase_key.json")
default_app = initialize_app(cred)

def verify_firebase_token(id_token: str) -> Dict[str, Any]:
    try:
        decoded_token: Dict[str, Any] = auth.verify_id_token(id_token)
        return decoded_token
    except (InvalidIdTokenError, ExpiredIdTokenError) as e:
        raise ValueError("Invalid or expired Firebase token") from e