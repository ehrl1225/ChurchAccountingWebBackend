from passlib.hash import pbkdf2_sha256
import hmac, hashlib
from common.env import settings
from fastapi import Request
from typing import Optional


def hash_password(password: str) -> str:
    return pbkdf2_sha256.hash(password)

def verify_password(password: str, hashed_password: str) -> bool:
    return pbkdf2_sha256.verify(password, hashed_password)

def hash_jwt_token(token: str) -> str:
    return hmac.new(settings.SERVER_PEPPER, token.encode(), hashlib.sha256).hexdigest()

def verify_jwt_token(token: str, hashed_token:str) -> bool:
    return hashed_token == hash_jwt_token(token)

def get_client_ip(request: Request) -> Optional[str]:
    for header in ("cf-connecting-ip", "true-client-ip", "x-real-ip", "x-forwarded-for"):
        value = request.headers.get(header)
        if value:
            if header == "x-forwarded-for":
                return value.split(",")[0].strip()
            return value.strip()
    return request.client.host

def get_user_agent(request: Request) -> Optional[str]:
    return request.headers.get("User-Agent")