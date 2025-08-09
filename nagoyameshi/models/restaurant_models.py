from django.db import models
from django.utils.crypto import get_random_string
import os
from .restaurant_models import *

def create_id():
    return get_random_string(22)


def upload_image_to(instance, filename):
    restaurant_id = instance.id
    return os.path.join("static", "restaurant", restaurant_id, filename)


###タグ###
class Tag(models.Model):
    slug = models.CharField(max_length=32, primary_key=True)
    name = models.CharField(max_length=32)
 
    def __str__(self):
        return self.name

###カテゴリ###
class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


###飲食店の基本情報###
class Restaurant(models.Model):
    id = models.CharField(default=create_id, primary_key=True, max_length=22, editable=False)
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True
    )  # related_name="restaurant")
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=20, blank=True)
    #price = models.CharField(max_length=20, blank=True)
    #post_code = models.CharField(max_length=20, blank=True)
    #start_time = models.CharField(max_length=20, blank=True)
    #end_time = models.CharField(max_length=20, blank=True)
    #closed_day = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        default="", blank=True, upload_to=upload_image_to)
    tags = models.ManyToManyField(Tag)
     # Staticの使い方確認

    def __str__(self):
        return self.name


###Udemy参考
""" class Item(models.Model):
    id = models.CharField(default=create_id, primary_key=True,
                          max_length=22, editable=False)
    name = models.CharField(default='', max_length=50)
    description = models.TextField(default='', blank=True)
    is_published = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(default="", blank=True,
                              upload_to=upload_image_to)
 
    def __str__(self):
        return self.name """
