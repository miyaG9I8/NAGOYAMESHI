from django.db import models
from django.utils.crypto import get_random_string
import os
from .restaurant_models import *
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator,MinValueValidator,MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone 


#User = get_user_model()

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
    price = models.CharField(max_length=20, blank=True)
    post_code = models.CharField(max_length=20, blank=True)
    start_time = models.TimeField(max_length=20, blank=True)
    end_time = models.TimeField(max_length=20, blank=True)
    closed_day = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(
        default="", blank=True, upload_to="nagoyameshi/restaurant/image/")
    tags = models.ManyToManyField(Tag)
     # Staticの使い方確認

    def __str__(self):
        return self.name


class Review(models.Model):
    created_date = models.DateTimeField(verbose_name="作成日時", auto_now_add=True)
    user = models.ForeignKey("nagoyameshi.CustomUser", verbose_name="レビューユーザー", on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, verbose_name="対象飲食店", on_delete=models.CASCADE)
    #comment = models.TextField(verbose_name="コメント")  --->contentに変更
    star = models.IntegerField(verbose_name="評価", validators=[MinValueValidator(1),MaxValueValidator(5)])
    subject     = models.CharField(verbose_name="件名", max_length=100,blank=True, default="")
    content     = models.TextField(verbose_name="内容", max_length=100, blank=True, default="")


    def star_icon(self):
        dic                 = {}
        dic["true_star"]    = self.stars * " "
        dic["false_star"]   = (5-self.stars)* " "

        return dic

class Reservation(models.Model):
    date = models.DateTimeField(verbose_name="予約日時")
    user = models.ForeignKey("nagoyameshi.CustomUser", verbose_name="予約者", on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, verbose_name="対象飲食店", on_delete=models.CASCADE)
    people = models.PositiveIntegerField(verbose_name="予約人数")

    def clean(self):
        super().clean()

        #予約人数が空かをチェック
        if self.people == None:
          raise ValidationError("予約人数を入れてください　")
        
        now = timezone.now()

        # 検証用にrestaurantがまだセットされていない段階なら何もしないで終了
        if not self.restaurant_id:
            return

        #営業時間チェック　営業時間をご確認くださいと表示する
        start = self.restaurant.start_time
        end   = self.restaurant.end_time

        if self.date.time() < start or self.date.time() > end:
            raise ValidationError("営業時間をご確認ください")
    

class Favorite(models.Model):
    user = models.ForeignKey("nagoyameshi.CustomUser", on_delete=models.CASCADE, related_name="favorites")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)

    # 同じユーザーが同じ店を複数回登録できないようにする
    class Meta:
        unique_together = ("user", "restaurant")  

    def __str__(self):
        return f"{self.user.email} → {self.restaurant.name}"
    
