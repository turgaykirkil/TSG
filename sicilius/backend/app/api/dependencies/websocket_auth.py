import logging
from fastapi import WebSocket, Depends, HTTPException, status
from app.core import security
from app.core.config import settings
from app.core.dependencies import get_supabase_client
from app.crud.user import get_user_by_email
from app.models.user import User
from app.models.token import TokenPayload
from jose import JWTError
from pydantic import ValidationError

logger = logging.getLogger(__name__)

async def websocket_auth(websocket: WebSocket) -> User:
    """
    Authenticates WebSocket connections.
    Authenticates WebSocket connections using the access_token cookie.
    This aligns with the HTTP-only cookie authentication used by the rest of the app.
    """
    token = websocket.cookies.get("fastapi-users-auth")
    source = "cookie"

    if not token:
        logger.error("WebSocket token not found in cookies. Checking query_params as a fallback.")
        token = websocket.query_params.get("token")
        source = "query_params"

    if not token:
        logger.error("WebSocket token not found in cookies or query_params. Checking headers as a final fallback.")
        auth_header = websocket.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            source = "Authorization header"

    if not token:
        logger.error("Authentication token not found in query params or headers. Closing connection.")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Token not provided")
        # We can't raise HTTPException after closing, but we can return to stop execution.
        return

    logger.info(f"Token found in {source}. Attempting to validate...")

    try:
        payload = security.decode_access_token(token)
        token_data = TokenPayload(**payload)
        logger.info(f"Token payload decoded successfully for user: {token_data.sub}")
    except (JWTError, ValidationError) as e:
        logger.error(f"Token validation failed: {e}. Closing connection.")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Invalid token")
        return

    try:
        # We need a Supabase client instance here, not a dependency
        supabase_client = get_supabase_client()
        user = get_user_by_email(supabase=supabase_client, email=token_data.sub)
    except Exception as e:
        logger.error(f"Error fetching user from database: {e}. Closing connection.")
        await websocket.close(code=status.WS_1011_INTERNAL_ERROR, reason="Database error")
        return

    if user is None:
        logger.error(f"User '{token_data.sub}' not found in the database. Closing connection.")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="User not found")
        return

    if not user.is_active:
        logger.warning(f"User '{user.email}' is inactive. Closing connection.")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION, reason="Inactive user")
        return

    logger.info(f"WebSocket authentication successful for user: {user.email}")
    return user
