from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from allauth.account import app_settings as allauth_settings
from allauth.account.adapter import get_adapter
from allauth.account.utils import complete_signup, perform_login
from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.contrib.auth import logout as django_logout
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

User = get_user_model()

class AllauthRegisterView(generics.CreateAPIView):
    """
    Registration endpoint using django-allauth
    """
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        data = request.data
        email = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')

        # Validate passwords
        if password1 != password2:
            return Response(
                {'error': 'Passwords do not match'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            validate_password(password1)
        except ValidationError as e:
            return Response(
                {'error': e.messages},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check if user exists
        if User.objects.filter(email=email).exists():
            return Response(
                {'error': 'User with this email already exists'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Create user using allauth
        try:
            user = User.objects.create_user(
                email=email,
                password=password1,
                username=email  # Use email as username if needed
            )
            
            # Create email address record
            EmailAddress.objects.create(
                user=user,
                email=email,
                primary=True,
                verified=allauth_settings.EMAIL_VERIFICATION == 'none'
            )

            # Complete signup
            complete_signup(request, user, 
                          allauth_settings.EMAIL_VERIFICATION, 
                          None)

            # Create or get token
            token, created = Token.objects.get_or_create(user=user)

            return Response({
                'key': token.key,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                }
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )


class AllauthLoginView(APIView):
    """
    Login endpoint using django-allauth
    """
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response(
                {'error': 'Email and password are required'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Authenticate user using allauth
        from django.contrib.auth import authenticate
        user = authenticate(request, username=email, password=password)

        if user is None:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        # Perform login using allauth
        perform_login(request, user, 
                     email_verification=allauth_settings.EMAIL_VERIFICATION,
                     redirect_url=None)

        # Get or create token
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'key': token.key,
            'user': {
                'id': user.id,
                'email': user.email,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        })


class AllauthLogoutView(APIView):
    """
    Logout endpoint
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Delete token
        try:
            request.user.auth_token.delete()
        except:
            pass
        
        # Logout using allauth
        django_logout(request)
        
        return Response(
            {'message': 'Successfully logged out'},
            status=status.HTTP_200_OK
        )


class AllauthUserView(APIView):
    """
    Get current user info
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({
            'id': request.user.id,
            'email': request.user.email,
            'username': request.user.username,
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'is_verified': EmailAddress.objects.filter(
                user=request.user, 
                verified=True
            ).exists(),
        })


class AllauthUpdateUserView(APIView):
    """
    Update user profile
    """
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        data = request.data

        # Update fields
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'username' in data:
            user.username = data['username']

        user.save()

        return Response({
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'first_name': user.first_name,
            'last_name': user.last_name,
        })


class AllauthChangePasswordView(APIView):
    """
    Change password using allauth
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password1 = request.data.get('new_password1')
        new_password2 = request.data.get('new_password2')

        # Check old password
        if not user.check_password(old_password):
            return Response(
                {'error': 'Current password is incorrect'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Check new passwords match
        if new_password1 != new_password2:
            return Response(
                {'error': 'New passwords do not match'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Validate new password
        try:
            validate_password(new_password1, user)
        except ValidationError as e:
            return Response(
                {'error': e.messages},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Set new password
        user.set_password(new_password1)
        user.save()

        # Delete old token and create new one
        try:
            user.auth_token.delete()
        except:
            pass
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'message': 'Password changed successfully',
            'key': token.key
        })