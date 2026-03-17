from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import CreateUserSerializer, LoginSerializer
from .permissions import IsAdmin, IsLecturer
from .models import CustomUser


class CreateLecturerView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    'status': 'error',
                    'message': 'Could not create lecturer account.',
                    'errors': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Force role to lecturer regardless of what was sent
        user = serializer.save(role='lecturer')

        return Response(
            {
                'status': 'success',
                'message': 'Lecturer account created successfully.',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'full_name': f"{user.first_name} {user.last_name}".strip(),
                },
            },
            status=status.HTTP_201_CREATED,
        )


class CreateStudentView(APIView):
    permission_classes = [IsAuthenticated, IsLecturer]

    def post(self, request):
        serializer = CreateUserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    'status': 'error',
                    'message': 'Could not create student account.',
                    'errors': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Force role to student regardless of what was sent
        user = serializer.save(role='student')

        return Response(
            {
                'status': 'success',
                'message': 'Student account created successfully.',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'role': user.role,
                    'full_name': f"{user.first_name} {user.last_name}".strip(),
                },
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                {
                    'status': 'error',
                    'message': 'Login failed.',
                    'errors': serializer.errors,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = serializer.validated_data['user']

        # Generate tokens
        refresh = RefreshToken.for_user(user)
        access_token = refresh.access_token

        # Inject custom claims into the access token payload
        # so the frontend can decode role without an extra API call
        access_token['role'] = user.role
        access_token['username'] = user.username

        return Response(
            {
                'status': 'success',
                'message': 'Login successful.',
                'data': {
                    'access': str(access_token),
                    'refresh': str(refresh),
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'role': user.role,
                        'full_name': f"{user.first_name} {user.last_name}".strip(),
                    },
                },
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """
    POST /api/v1/auth/logout/

    Blacklists the refresh token so it
    cannot be used to generate new access tokens.
    Requires the user to be authenticated.

    Request body:
    {
        "refresh": "<refresh token>"
    }
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response(
                {
                    'status': 'error',
                    'message': 'Refresh token is required.',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception:
            return Response(
                {
                    'status': 'error',
                    'message': 'Invalid or expired token.',
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        return Response(
            {
                'status': 'success',
                'message': 'Logged out successfully.',
            },
            status=status.HTTP_200_OK,
        )