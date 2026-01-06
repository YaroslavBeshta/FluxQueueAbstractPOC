import os

from dotenv import load_dotenv


def load_environment_variables():
    # Load environment variables based on ENVIRONMENT variable
    env = os.getenv("ENVIRONMENT", "dev").lower()
    if env == "prod" or env == "production":
        load_dotenv(".env.prod")
    elif env == "dev" or env == "development":
        load_dotenv(".env.dev")
    else:
        # Fallback to default .env file
        load_dotenv()
