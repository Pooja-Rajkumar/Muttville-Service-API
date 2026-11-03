import os

if os.environ.get("APP_ENV").lower() == "local":
    IS_LOCAL = True
else:
    IS_LOCAL = False