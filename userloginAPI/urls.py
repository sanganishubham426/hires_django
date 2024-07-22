from django.urls import path
from . import views

# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView


urlpatterns = [
    path('registerUser', views.UserRegisterAPI.as_view(), name="registerPage"),
    path('loggedInUpdateUser', views.UserloggedInUpdateAPI.as_view(), name="loggedInUpdateUserPage"),
    path('emailVerificationUser', views.EmailVerificationAPI.as_view(), name="emailVerficationPage"),



    path('UserIdGet', views.UserIdGetAPI.as_view(), name="UserIdGetPage"),

    path('emailVerificationCompletion', views.EmailVerificationCompletionAPI.as_view(), name="emailVerficationCompletionPage"),

    path('loginUser', views.UserLoginAPI.as_view(), name="loginPage"),
    path('logoutUser', views.UserLogoutAPI.as_view(), name="logoutPage"),

    path('forgetPasswordUser', views.UserForgetPasswordAPI.as_view(), name="ForgetPasswordPage"),
    path('forgetPasswordUserChanged', views.ForgotPasswordChangedAPI.as_view(), name="ForgetPasswordChangedPage"),
    path('changePasswordUser', views.UserChangePasswordAPI.as_view(), name = "ChangePasswordPage"),

    path('UserEditProfile', views.UserEditProfileAPI.as_view(), name = "UserEditProfilePage"),

    path('ViewUserProfile', views.ViewUserProfileAPI.as_view(), name = "ViewUserProfilePage"),

    path('getuserdata',views.GetUserdataAPI.as_view(),name="UserGetDataPage"),



]