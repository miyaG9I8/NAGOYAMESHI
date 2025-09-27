from django.urls import path
#from nagoyameshi import views
from . import views
from django.contrib.auth.views import LogoutView 
from nagoyameshi.views.account_views import SignupView, PremiumView
from nagoyameshi.views.restaurant_views import ReservationView

app_name    = "nagoyameshi"
urlpatterns = [
    #Account
    path("signup/", SignupView.as_view(), name="signup"),
    path("signup_premium/", PremiumView.as_view(), name="signup_premium"),
    path("login/", views.login, name="login"),  #loginとsignupもlogout・profileの書きたに統一した方がいいかも
    path("logout/", views.logout, name="logout"), 
    path('profile/', views.ProfileUpdateView.as_view(),name='profile'),
    path("password_change/", views.password_change, name="password_change"),
    path("password_change/done/", views.password_change_done, name="password_change_done"),
    path("password_reset/", views.password_reset, name="password_reset"),
    path("password_reset/done/", views.password_reset_done, name="password_reset_done"),
    path("reset/<uidb64>/<token>/", views.password_reset_confirm, name="password_reset_confirm"),
    path("reset/done/", views.password_reset_complete, name="password_reset_complete"),

    #Restaurant_detail
    path('restaurant/<str:pk>/', views.RestaurantDetailView.as_view(),name="restaurant_detail"),  #nameを追加
    path('restaurant_list/', views.RestaurantListView.as_view(),name="restaurant_list"),
    path("restaurant/<int:pk>/reservation/", ReservationView.as_view(), name="reservation"),

    #トップページ
    path('', views.IndexListView.as_view(),name="index" ), 
]