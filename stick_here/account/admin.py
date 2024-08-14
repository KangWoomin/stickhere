from django.contrib import admin
from .models import User,UserProfile,HobbyCategory,UserHobby_click,TextBoard,ShortMovieBoard,FriendRequst,Friendship


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['email','nickname','number','is_active']
    list_display_links = ['email','nickname']
    search_fields = ['email','nickname']

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','text','location']
    list_display_links =['user','text']

admin.site.register(Friendship)
admin.site.register(FriendRequst)
admin.site.register(ShortMovieBoard)
admin.site.register(TextBoard)
admin.site.register(UserHobby_click)
admin.site.register(HobbyCategory)
admin.site.register(UserProfile)
admin.site.register(User)