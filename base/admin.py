from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Profile, FriendRequest

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser')
    list_display_links = ('id', 'username', 'email')
    search_field = ('id', 'username', 'email')
    list_per_page = 25

admin.site.register(User, UserAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user',)
    list_display_links = ('user',)
    search_field = ('user')
    list_per_page = 25

admin.site.register(Profile, ProfileAdmin)

class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('from_user', 'to_user', 'request_date', 'is_accepted', 'is_declined', 'is_canceled')
    list_display_links = ('from_user', 'to_user', 'request_date', 'is_accepted', 'is_declined', 'is_canceled')
    search_field = ('from_user', 'to_user','request_date', 'is_accepted', 'accepted_on', 'is_declined', 'is_canceled')
    list_per_page = 25

admin.site.register(FriendRequest, FriendRequestAdmin)