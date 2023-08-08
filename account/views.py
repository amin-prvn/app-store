from rest_framework.views import APIView
from rest_framework import permissions, generics
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer


class RegisterView(generics.CreateAPIView):
    permission_classes=[permissions.AllowAny]
    queryset = User.objects.all()    
    serializer_class = RegisterSerializer


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    # TODO -> Implement Expire refresh token
    pass


class ProfileView(generics.RetrieveUpdateAPIView):
    permission_classes=[permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    def get_object(self):
        return self.request.user