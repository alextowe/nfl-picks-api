from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Matchup
from django.contrib.auth import get_user_model
User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser')
    list_display_links = ('id', 'username', 'email')
    search_field = ('id', 'username', 'email')
    list_per_page = 25

admin.site.register(User, UserAdmin)

class MatchupAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_name', 'week', 'year', 'away_score', 'home_score', 'completed')
    list_display_links = ('id', 'short_name', 'week', 'year','away_score', 'home_score', 'completed')
    search_field = ('id', 'short_name', 'week', 'year', 'completed')
    list_per_page = 25

admin.site.register(Matchup, MatchupAdmin)