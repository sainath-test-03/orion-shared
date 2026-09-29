import base64
import hashlib
import hmac
import json
import time


def identity(token, key):
    if not key:
        raise ValueError('Identity service is unavailable')
    body, supplied = token.split('.', 1)
    expected = base64.urlsafe_b64encode(hmac.new(key.encode(), body.encode(), hashlib.sha256).digest()).decode().rstrip('=')
    if not hmac.compare_digest(supplied, expected):
        raise ValueError('Invalid session')
    claims = json.loads(base64.urlsafe_b64decode(body + '=' * (-len(body) % 4)))
    if claims['expires'] <= time.time() or claims['audience'] != 'orion':
        raise ValueError('Expired session')
    if not all(isinstance(claims.get(k), str) and claims[k] for k in ('user', 'tenant', 'role')):
        raise ValueError('Incomplete session')
    return claims
