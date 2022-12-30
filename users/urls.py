from django.urls import path
from django.contrib.auth.views import LogoutView
from django.conf import settings
from .views import (EmployeeSigUpFormView,
                    SignInView,
                    ProfileEmployeeList,
                    ProfileEmployeeDetail,
                    ProfileEmployeeInlineCreate,
                    ClientSigUpFormView,
                    ClientSignInView,
                    ProfileClientCreateView,
                    )


urlpatterns = [
    path('EmployeeSignup/', EmployeeSigUpFormView.as_view(), name='Employee_Signup'),
    path('EmployeeSignin/', SignInView.as_view(), name='Employee_Signin'),
    path('EmployeeSignout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='Employee_Signout',),
    path('ProfileEmployee/', ProfileEmployeeInlineCreate.as_view(), name='profile_list'),
    path('ProfileEmployeeList/', ProfileEmployeeList.as_view(), name='ProfileEmployeeList'),
    path('ProfileEmployeeDetail/<int:pk>/', ProfileEmployeeDetail.as_view(), name='ProfileEmployeeDetail'),
    path('SigUpClientFormView/', ClientSigUpFormView.as_view(), name='SigUpClientFormView'),
    path('ClientSignInView/', ClientSignInView.as_view(), name='ClientSignInView'),
    path('ProfileClientCreateView/', ProfileClientCreateView.as_view(), name='ProfileClientCreateView')
]
