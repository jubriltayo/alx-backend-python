from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from .models import User



def create_user(validated_data):
    """
    Standard function to create a user with hashed password
    """
    try:
        # Hash the password before saving
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            phone_number=validated_data.get('phone_number', None),
            role=validated_data.get('role', 'guest')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    except Exception as e:
        raise ValidationError({"error": str(e)})


def generate_tokens_for_user(user):
    """
    Utilty function to generate tokens for a user
    """
    try:
        token = RefreshToken.for_user(user)
        return {
            "accessToken": str(token.access_token),
            "refreshToken": str(token)
        }
    except Exception as e:
        raise ValidationError({"error": f"Failed to generate tokens: {str(e)}"})


def authenticate_user(email, password):
    """
    Standard function to authenticate a user
    """
    from django.contrib.auth import authenticate
    user = authenticate(email=email, password=password)
    if user is None:
        raise AuthenticationFailed("Invalid credentials")
    if not user.is_active:
        raise AuthenticationFailed("User is inactive")
    return user


from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

class DebugJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        print("DEBUG: JWTAuthentication.authenticate called")
        header = self.get_header(request)
        if header is None:
            print("DEBUG: No Authorization header found")
            return None
        print(f"DEBUG: Authorization header: {header}")

        raw_token = self.get_raw_token(header)
        if raw_token is None:
            print("DEBUG: No raw token found in header")
            return None
        print(f"DEBUG: Raw token: {raw_token}")

        try:
            validated_token = self.get_validated_token(raw_token)
            print(f"DEBUG: Validated token: {validated_token}")
        except InvalidToken as e:
            print(f"DEBUG: Token validation failed: {str(e)}")
            return None

        return self.get_user(validated_token), validated_token
