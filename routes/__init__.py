from routes.auth import router as auth_router
from routes.chats import router as chats_router
from routes.messages import router as messages_router
from routes.upload import router as upload_router

__all__ = ["auth_router", "chats_router", "messages_router", "upload_router"]
