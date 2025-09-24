from .models import CustomUser,Restaurant, Review, Category
from django.contrib.auth.forms import UserCreationForm
from django import forms

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model   = CustomUser
        fields  = ("username","email", )


class RestaurantCategoryForm(forms.ModelForm):
    class Meta:
        model   = Restaurant
        fields  = [ "name" ]   

class RestaurantCategorySearchForm(forms.ModelForm):
    class Meta:
        model   = Restaurant
        fields  = [ "category" ]


class ReviewForm(forms.ModelForm):
    class Meta:
        model	= Review
        fields	= [ "star", 
                  "restaurant", 
                  "subject", 
                  "content" ]

class CategoryForm(forms.ModelForm):
    class Meta:
        model	= Category
        fields	= [ "name" ]

