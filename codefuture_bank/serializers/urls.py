from django.urls import path

from serializers import views


urlpatterns = [
    path("phone_serializer/", views.phone_serializer_view),
    path("fcs_serializer/", views.fcs_serializer_view)

]