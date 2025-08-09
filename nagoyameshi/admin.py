from django.contrib import admin
from nagoyameshi.models import Restaurant, Category, Tag
from django.contrib.auth.models import Group
 
 
class TagInline(admin.TabularInline):
    model = Restaurant.tags.through
 
 
class RestaurantAdmin(admin.ModelAdmin):
    inlines = [TagInline]
    exclude = ['tags']
 
 
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.unregister(Group)




