from django.shortcuts import render, redirect
from django.conf import settings
from django.urls import reverse_lazy
from django.http import HttpResponseNotAllowed
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView,LogoutView,PasswordChangeView,PasswordChangeDoneView,PasswordResetView,PasswordResetDoneView,PasswordResetConfirmView,PasswordResetCompleteView
from django.views.generic import CreateView, UpdateView
from ..forms import SignupForm
from ..models import Profile

from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
#import stripe


class SignupView(CreateView):

    form_class      = SignupForm
    success_url     = reverse_lazy("login")
    template_name   = "pages/signup.html"

    # 認証済みの状態でリクエストした時、LOGIN_REDIRECT_URL へリダイレクトさせる
    def dispatch(self, request, *args, **kwargs):
        #if self.request.user.is_authenticated:
            #return redirect(settings.LOGIN_REDIRECT_URL)　#マイページから有料会員登録に飛ばすため
        return super().dispatch(request, *args, **kwargs)

signup  = SignupView.as_view()


class CustomLoginView(LoginView):

    template_name = "pages/login.html"

    # 認証済みの状態でリクエストした時、LOGIN_REDIRECT_URL へリダイレクトさせる
    def dispatch(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect(settings.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)
    
    def get_success_url(self):
        return "/"

login   = CustomLoginView.as_view()

class CustomLogoutView(LogoutView):

    template_name = "pages/logout.html"

    def get(self, request, *args, **kwargs):
        return HttpResponseNotAllowed(permitted_methods=['POST'])

logout  = CustomLogoutView.as_view()


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = Profile
    template_name = 'pages/profile.html'
    fields = ('name', 'zipcode','email','address', 'tel')
    success_url = '/profile/'

    def get_object(self, queryset=None):
        # ログインユーザーのProfileを取得、なければ作成
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
    


class PremiumView(View):
    def get(self, request, *args, **kwargs):
        return render(request, "pages/signup_premium.html")
                

premium     = PremiumView.as_view()
        



password_change             = PasswordChangeView.as_view()
password_change_done        = PasswordChangeDoneView.as_view()
password_reset              = PasswordResetView.as_view()
password_reset_done         = PasswordResetDoneView.as_view()
password_reset_confirm      = PasswordResetConfirmView.as_view()
password_reset_complete     = PasswordResetCompleteView.as_view()