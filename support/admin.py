from django.contrib import admin

# Register your models here.
# support/admin.py
from django.contrib import admin
from .models import SupportCategory, SupportTicket

@admin.register(SupportCategory)
class SupportCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('subject', 'user', 'category', 'status', 'created_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('subject', 'message', 'user__username')
    readonly_fields = ('created_at', 'updated_at')