from django.contrib import admin
from .models import Email

# Register your models here.

@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = ('sender', 'recipient', 'subject', 'timestamp')
    search_fields = ('sender__username', 'recipient__username', 'subject')
    list_filter = ('timestamp',)
    ordering = ('-timestamp',)

    def has_add_permission(self, request):
        return False