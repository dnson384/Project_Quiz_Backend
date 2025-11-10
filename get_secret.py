import secrets

jwt_secret_urlsafe = secrets.token_urlsafe(32)

print(jwt_secret_urlsafe)