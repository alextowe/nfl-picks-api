from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from base.models import Matchup, PickGroup, Pick
from django.contrib.auth import get_user_model
User = get_user_model()


class UserAdmin(UserAdmin):
    """
    Admin settings for user model that includes email during signup and adds a 'following' list in the admin detail.
    """

    list_display = ('id', 'username', 'email', 'is_active', 'is_staff', 'is_superuser')
    list_display_links = ('id', 'username', 'email')
    search_field = ('id', 'username', 'email')
    ordering = ('id',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (_('Following list'), {'fields': ('following',)}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
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
    """
    Admin settings for the matchup model.
    """

    list_display = ('id', 'short_name', 'week', 'year', 'away_score', 'home_score', 'date', 'last_updated',  'completed')
    list_display_links = ('id', 'short_name', 'week', 'year','away_score', 'home_score', 'date', 'last_updated', 'completed')
    search_field = ('id', 'short_name', 'week', 'year', 'completed', 'last_updated', 'date')
    ordering = ('id',)
    list_per_page = 25

admin.site.register(Matchup, MatchupAdmin)

class PickGroupAdmin(admin.ModelAdmin):
    """
    Admin settings for the pick group model.
    """

    list_display = ('id', 'title', 'owner')
    list_display_links = ('id', 'title', 'owner')
    search_field = ('id', 'title', 'owner')
    ordering = ('id',)
    list_per_page = 25

admin.site.register(PickGroup, PickGroupAdmin)

class PickAdmin(admin.ModelAdmin):
    """
    Admin settings for the pick group model.
    """

    list_display = ('id', 'owner', 'pick_group', 'matchup', 'is_correct')
    list_display_links = ('id', 'owner', 'pick_group', 'matchup', 'is_correct')
    search_field = ('id', 'owner', 'pick_group', 'matchup', 'is_correct')
    ordering = ('id',)
    list_per_page = 25

admin.site.register(Pick, PickAdmin)