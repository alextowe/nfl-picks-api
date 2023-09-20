from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import MatchUp
from django.contrib.auth import get_user_model
User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser')
    list_display_links = ('id', 'username', 'email')
    search_field = ('id', 'username', 'email')
    list_per_page = 25

admin.site.register(User, UserAdmin)

class MatchUpAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_name', 'week', 'year')
    list_display_links = ('id', 'short_name', 'week', 'year')
    search_field = ('id', 'short_name', 'week', 'year')
    list_per_page = 25

admin.site.register(MatchUp, MatchUpAdmin)