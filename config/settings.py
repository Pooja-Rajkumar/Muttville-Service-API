import os

IS_LOCAL = os.getenv("APP_ENV", "prod").lower() == "local"