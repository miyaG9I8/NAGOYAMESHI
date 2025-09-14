from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model   = CustomUser
        fields  = ("username","email", )