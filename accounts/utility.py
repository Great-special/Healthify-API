from rest_framework_simplejwt.tokens import AccessToken
from .models import CustomUser

def get_user_from_token(request):
    token = get_access_token(request)
    if token:
        try:
            access_token = AccessToken(token)
            user_id = access_token['user_id']  # Extract user ID from the token
            user = CustomUser.objects.get(id=user_id)  # Fetch the user from the database
            return user
        except Exception as e:
            print(f"Error decoding token: {e}")
    return None

def get_access_token(request):
    auth_header = request.headers.get('Authorization')
    if auth_header and auth_header.startswith('Bearer '):
        return auth_header.split(' ')[1]  # Extract the token part
    return None