from django.urls import include, path

app_name = "api"

urlpatterns = [
    path('', include('user_auth.api.urls')),
]