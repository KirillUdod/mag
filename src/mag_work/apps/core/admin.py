from django.contrib import admin
from core.models import IndexBlock


class IndexBlockAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'text')
    list_display_links = ('id', 'title', 'text')
    actions = None


    def has_add_permission(self, request):
        return True

    def has_delete_permission(self, request, obj=None):
        return True

admin.site.register(IndexBlock, IndexBlockAdmin)