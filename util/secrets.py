import hashlib

__all__ = ["encrypt"]


def encrypt(pwd: str) -> str:
    return hashlib.sha256(pwd.encode(encoding="utf-8")).hexdigest()
