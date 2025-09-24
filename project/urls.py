"""
URL configuration for nagoyameshi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

""""
from django.contrib import admin
from django.urls import path, include
from nagoyameshi import views
from django.contrib.auth.views import LogoutView 
from nagoyameshi.views.account_views import SignupView, PremiumView

app_name    = "nagoyameshi"
urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("nagoyameshi.urls", namespace="nagoyameshi")),

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
    path('restaurant/<str:pk>/', views.RestaurantDetailView.as_view(),name="restaurant"),  #nameを追加
    path('restaurant_list/', views.RestaurantListView.as_view(),name="restaurant_list"),

    #トップページ
    path('', views.IndexListView.as_view(),name="index" ), 
]

"""
#nagoyameshi直下のurls.pyに記載した↑

from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    #path('accounts/', include("accounts.urls")),
    path('', include("nagoyameshi.urls",namespace="nagoyameshi")),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


