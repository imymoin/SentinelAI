import os

from dotenv import load_dotenv
from fastapi import HTTPException, Security
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

load_dotenv()

security = HTTPBearer()


async def verify_api_key(
    credentials: HTTPAuthorizationCredentials = Security(security),
):
    api_key = os.getenv("SENTINEL_API_KEY")

    if not api_key:
        raise HTTPException(
            status_code=500,
            detail="API key is not configured."
        )

    if credentials.credentials != api_key:
        raise HTTPException(
            status_code=401,
            detail="Invalid API key."
        )

    return True