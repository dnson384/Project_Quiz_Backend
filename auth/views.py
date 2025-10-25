from rest_framework.response import Response
from rest_framework import status, generics

from .serializers import RegisterWithEmailSerializer, LoginWithEmailSerializer


class RegisterWithEmailView(generics.CreateAPIView):
    serializer_class = RegisterWithEmailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        self.perform_create(serializer)

        return Response(
            {"message": "Register Successful"}, status=status.HTTP_201_CREATED
        )


class LoginWithEmailView(generics.CreateAPIView):
    serializer_class = LoginWithEmailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        return Response({"message": "Login Successful"}, status=status.HTTP_200_OK)
