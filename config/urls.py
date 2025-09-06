from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from configapp.views import SendCodeView, VerifyCodeView
from configapp.views import LoginUser, RegisterUser, ToDoListView, ToDoDetailView

schema_view = get_schema_view(
   openapi.Info(
      title="My API",
      default_version='v1',
      description="ToDo Project API",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@example.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)

api_urlpatterns = [
    # JWT
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # Custom auth
    path("login/", LoginUser.as_view(), name="login"),
    path("register/", RegisterUser.as_view(), name="register"),

    # ToDo endpoints
    path("todos/", ToDoListView.as_view(), name="todo_list"),
    path("todos/<int:pk>/", ToDoDetailView.as_view(), name="todo_detail"),

# JWT
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # Custom auth
    path("login/", LoginUser.as_view(), name="login"),
    path("register/", RegisterUser.as_view(), name="register"),

    # ToDo endpoints
    path("todos/", ToDoListView.as_view(), name="todo_list"),
    path("todos/<int:pk>/", ToDoDetailView.as_view(), name="todo_detail"),

    # 📌 SMS auth
    path("send-code/", SendCodeView.as_view(), name="send_code"),
    path("verify-code/", VerifyCodeView.as_view(), name="verify_code"),
]



urlpatterns = [
    path("admin/", admin.site.urls),

    # Swagger
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui"),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),

    # API
    path("api/", include(api_urlpatterns)),
]