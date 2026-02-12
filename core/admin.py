from django.contrib import admin
from .models import Member

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'qr_code', 'current_streak', 'last_checkin')
    search_fields = ('name', 'qr_code')
    list_filter = ('last_checkin',)