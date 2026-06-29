import os
from dotenv import load_dotenv

load_dotenv()

REQUIRED_VARS = [
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "KAFKA_BOOTSTRAP_SERVERS",
]


class CredentialManager:
    def __init__(self, required=None):
        self.required = required or REQUIRED_VARS

    def get(self, key, default=None):
        return os.getenv(key, default)

    def require(self, key):
        val = os.getenv(key)
        if not val:
            raise ValueError(f"Missing required environment variable: {key}")
        return val

    def validate(self):
        missing = [v for v in self.required if not os.getenv(v)]
        if missing:
            raise EnvironmentError(
                f"Missing required env vars: {', '.join(missing)}"
            )
        return True


if __name__ == "__main__":
    cm = CredentialManager()
    cm.validate()
    print("All required credentials present.")
