from django.urls import path
from django.views.generic.base import TemplateView

from main import views

urlpatterns = [
    path(
        "help-wanted/<int:pk>/delete/",
        views.main.AidRequestDeleteView.as_view(),
        name="aidrequest_delete",
    ),
    path(
        "help-wanted/<int:pk>/close/",
        views.main.aidrequest_close,
        name="aidrequest_close",
    ),
    path(
        "help-wanted/<int:pk>/edit/",
        views.main.AidRequestUpdateView.as_view(),
        name="aidrequest_update",
    ),
    path(
        "help-wanted/create/",
        views.main.AidRequestCreateView.as_view(),
        name="aidrequest_create",
    ),
    path(
        "help-wanted/<int:pk>/",
        views.main.AidRequestDetailForHospital.as_view(),
        name="aidrequestforhospital_detail",
    ),
    path(
        "help-wanted/list/", views.main.AidRequestListForHospital.as_view(), name="aidrequestforhospital_list"
    ),
    path("signup/step2/", views.main.SignupStep2.as_view(), name="signup_step2"),
    path(
        "help-needed/aidrequests/<int:pk>/",
        views.main.AidRequestDetailForDonor.as_view(),
        name="aidrequestfordonor_detail",
    ),
    path(
        "help-needed/hospitals/<int:pk>/", views.main.HospitalDetailForDonor.as_view(), name="hospitalfordonor_detail"
    ),
    path(
        "help-needed/map/", views.main.HospitalListForDonor.as_view(), name="hospitalfordonor_list"
    ),
    path(
        "help-needed/list/", views.main.AidRequestListForDonor.as_view(), name="aidrequestfordonor_list"
    ),
    path("signup/", views.user.Signup.as_view(), name="signup"),
    path("", views.main.home),
]
