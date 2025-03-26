from urllib.parse import parse_qs
from channels.auth import AuthMiddlewareStack
from django.db import close_old_connections
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError 
from rest_framework_simplejwt.tokens import UntypedToken  
from jwt import decode as jwt_decode
from django.conf import settings
import logging


logger = logging.getLogger(__name__)

@database_sync_to_async
def get_user(validated_token):
    try:
        user = get_user_model().objects.get(uuid=validated_token["user_id"])
        return user
    except get_user_model().DoesNotExist:
        return AnonymousUser()

class JWTAuthMiddleware:

    """
    This class is responsible for validating the token for websocket and sets the validated user in scope
    """
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        try:
            
            # Close old database connections
            await database_sync_to_async(close_old_connections)()

            token = None

            
            
            #if not token:
            query_params = parse_qs(scope["query_string"].decode("utf8"))
            token = query_params.get("token", [None])[0]
        
            # Validate the token
            if token:
                try:
                    if hasattr(settings, 'SIMPLE_JWT'):
                        validated_token = UntypedToken(token)
                    else:  # Manual JWT decoding
                        validated_token = jwt_decode(token, settings.SECRET_KEY, algorithms=["HS256"])
                except (InvalidToken, TokenError):
                    logger.error("Invalid token")
                    return None  # Reject connection
                
                try:
                    # Get the user from the validated token
                    user = await get_user(validated_token)
                except RuntimeError as e:
                    logger.error(f"Runtime error during get_user: {e}")
                    scope["user"] = AnonymousUser()

                except Exception as e:
                    logger.error("Unexpected error retrieving user",exc_info=e)
                    scope['user'] = AnonymousUser()
            else:
                user = AnonymousUser()

            # Set the user on the scope and proceed
            scope["user"] = user
            return await self.inner(scope, receive, send)
        except Exception as e:
            logger.error("Error in JWTAuthMiddleware", exc_info=e)
            return None
        
            


def JWTAuthMiddlewareStack(inner):
    return JWTAuthMiddleware(AuthMiddlewareStack(inner))

       