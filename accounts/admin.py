from django.contrib import admin
from . models import Accounts,UserProfile
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html
# Register your models here.


class AccountsAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name',
                    'username', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_pic.url))
    thumbnail.short_description = 'Profile Pic'
    list_display=("thumbnail","user","city","state")
admin.site.register(Accounts, AccountsAdmin)
admin.site.register(UserProfile,UserProfileAdmin)



