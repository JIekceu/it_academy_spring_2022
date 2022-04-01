from django.contrib import admin
from . import models

# Register your models here.
# admin.site.register(models.Material)

admin.site.register(models.Comment)
"""нужно для возможности посмотреть комменты в админке, чтобы не делать отдельную
админ-панель для модераторов, а пустить их в админку с некоторыми ограничениями,
для чистки комментов"""

admin.site.register(models.Profile)

@admin.register(models.Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'material_type', 'publish')
    list_filter = ('material_type', 'created')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug': ('title', )}
    ordering = ('material_type', 'title')