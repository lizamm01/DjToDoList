from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from django.shortcuts import get_object_or_404
from rest_framework import status

from .models import *

from .serializers import *
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


class SendCodeView(APIView):
    def post(self, request):
        serializer = SendCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone"]

        code = PhoneVerfication.generate_code()
        PhoneVerfication.objects.create(phone=phone, code=code)

        # TODO: SMS yuborish (hozircha print)
        print(f"{phone} ga yuborilgan kod: {code}")

        return Response({"success": True, "detail": "Kod yuborildi."}, status=status.HTTP_200_OK)


class VerifyCodeView(APIView):
    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        phone = serializer.validated_data["phone"]
        code = serializer.validated_data["code"]

        try:
            record = PhoneVerfication.objects.filter(phone=phone, code=code).latest("created_at")
        except PhoneVerfication.DoesNotExist:
            return Response({"success": False, "detail": "Kod noto‘g‘ri."}, status=status.HTTP_400_BAD_REQUEST)

        if record.is_expired():
            return Response({"success": False, "detail": "Kod muddati tugagan."}, status=status.HTTP_400_BAD_REQUEST)


        user, created = User.objects.get_or_create(phone=phone, defaults={"username": phone})
        token = get_tokens_for_user(user)

        return Response({"success": True, "token": token}, status=status.HTTP_200_OK)
