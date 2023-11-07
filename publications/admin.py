from django.contrib import admin
from publications.models import *


# Register your models here.


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    """Публикации"""
    list_display = ('header', 'content', 'image', 'date_of_create', 'quantity_of_views')
    list_filter = ('date_of_create', 'quantity_of_views')
    search_fields = ('header', 'content', 'date_of_create',)
