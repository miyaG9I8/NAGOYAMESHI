from django.shortcuts import render
from django.views.generic import ListView, DetailView
from nagoyameshi.models import Restaurant


class IndexListView(ListView):
    model = Restaurant
    template_name = 'pages/index.html'

class RestaurantDetailView(DetailView):
    model = Restaurant
    template_name = 'pages/restaurant_detail.html'

