from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from nagoyameshi.models import Restaurant, Category, Tag, Review
from django.contrib.auth.models import Group
from .models import CustomUser, Reservation
from django.utils.translation import gettext_lazy as _
 
 
class TagInline(admin.TabularInline):
    model = Restaurant.tags.through

 
class RestaurantAdmin(admin.ModelAdmin):
    inlines = [TagInline]
    exclude = ['tags']

class CustomUserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', "customer")}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login',)}),
    )

    #管理サイトから追加するときのフォーム
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', "customer")
    search_fields = ('username', 'first_name', 'last_name', 'email')

class ReviewAdmin(admin.ModelAdmin):
    list_display	= [ "id", 
                        "user", 
                        "restaurant", 
                        "subject", 
                        "content", 
                        "created_at"]
    

class ReservationAdmin(admin.ModelAdmin):
    list_display = ("restaurant", "user", "date", "people")    


admin.site.register(CustomUser, CustomUserAdmin) 
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.unregister(Group)
admin.site.register(Review)
admin.site.register(Reservation, ReservationAdmin)




