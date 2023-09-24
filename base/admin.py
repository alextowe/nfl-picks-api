from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Matchup, PickGroup
from django.contrib.auth import get_user_model
User = get_user_model()


class UserAdmin(UserAdmin):
    list_display = ('id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser')
    list_display_links = ('id', 'username', 'email')
    search_field = ('id', 'username', 'email')
    ordering = ('id',)
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'email', 'password1', 'password2'),
            },
        ),
    )
    list_per_page = 25

admin.site.register(User, UserAdmin)

class MatchupAdmin(admin.ModelAdmin):
    list_display = ('id', 'short_name', 'week', 'year', 'away_score', 'home_score', 'date', 'completed')
    list_display_links = ('id', 'short_name', 'week', 'year','away_score', 'home_score', 'date', 'completed')
    search_field = ('id', 'short_name', 'week', 'year', 'completed', 'date')
    ordering = ('id',)
    list_per_page = 25

admin.site.register(Matchup, MatchupAdmin)

class PickGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'owner')
    list_display_links = ('id', 'title', 'owner')
    search_field = ('id', 'title', 'owner')
    ordering = ('id',)
    list_per_page = 25

admin.site.register(PickGroup, PickGroupAdmin)