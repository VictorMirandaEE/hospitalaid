from django.urls import path
from django.views.generic.base import TemplateView

from main import views

urlpatterns = [
    path("hospitals/", views.main.HospitalListView.as_view(), name="hospital_list"),
    path(
        "hospitals/create/",
        views.main.HospitalCreateView.as_view(),
        name="hospital_create",
    ),
    path(
        "hospitals/<int:pk>/",
        views.main.HospitalUpdateView.as_view(),
        name="hospital_update",
    ),
    path(
        "hospitals/<int:pk>/delete/",
        views.main.HospitalDeleteView.as_view(),
        name="hospital_delete",
    ),
    path(
        "aidrequests/", views.main.AidRequestListView.as_view(), name="aidrequest_list"
    ),
    path(
        "aidrequests/create/",
        views.main.AidRequestCreateView.as_view(),
        name="aidrequest_create",
    ),
    path(
        "aidrequests/<int:pk>/",
        views.main.AidRequestUpdateView.as_view(),
        name="aidrequest_update",
    ),
    path(
        "aidrequests/<int:pk>/delete/",
        views.main.AidRequestDeleteView.as_view(),
        name="aidrequest_delete",
    ),
    path(
        "aidresponses/for-me/",
        views.main.AidResponseForMeListView.as_view(),
        name="aidresponse_forme_list",
    ),
    path(
        "aidresponses/create/",
        views.main.AidResponseCreateView.as_view(),
        name="aidresponse_create",
    ),
    path("signup/", views.user.SignupView.as_view(), name="signup"),
    path("", TemplateView.as_view(template_name="home.html")),
]
