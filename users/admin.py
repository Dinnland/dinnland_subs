from django.contrib import admin

from users.models import User


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Клиенты"""
    list_display = ('phone', 'email', 'first_name', 'last_name',  'avatar', 'country', 'is_verified')
    # list_display = ('__all__',)
    search_fields = ('email', 'phone')

    moderator_readonly_fields = ('first_name', 'last_name', 'email', 'phone', 'avatar', 'country', 'is_verified',)
    # all_fields_my = ( 'phone', 'avatar', 'country', 'is_verified')
    # readonly_fields = all_fields_my

