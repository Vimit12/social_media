from django.urls import include, path

from .views import SignUp, UserNameAPI, LoginAPI

urlpatterns = [
    # path('admin/', admin.site.urls),
    # path('api-auth/', include('rest_framework.urls'))
    path("api/sign_up/", SignUp.as_view()),
    path("api/username/", UserNameAPI.as_view()),
    path("api/login/", LoginAPI.as_view()),
]
