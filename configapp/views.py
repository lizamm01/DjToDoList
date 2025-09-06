from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404

from .models import User, ToDoList
from .serializers import LoginSerializer, UserSerializer, ToDoListSerializer
from .make_token import get_tokens_for_user


class LoginUser(APIView):
    @swagger_auto_schema(request_body=LoginSerializer)
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(User, username=serializer.validated_data.get("username"))
        token = get_tokens_for_user(user)
        return Response(data=token)


class RegisterUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ToDoListView(generics.ListCreateAPIView):
    serializer_class = ToDoListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return ToDoList.objects.all()  # admin → barcha ishlari
        return ToDoList.objects.filter(user=user, bajarilgan=False)  # user → tugallanmaganlari

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ToDoDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ToDoListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_admin:
            return ToDoList.objects.all()
        return ToDoList.objects.filter(user=user, bajarilgan=False)
