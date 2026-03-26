from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin
from .models import Member, Streaks


@admin.register(Member)
class MemberAdmin(ModelAdmin):
    list_display = ('name', 'qr_code', 'streak_badge', 'mensuality_date', 'last_checkin')
    search_fields = ('name', 'qr_code', 'phone')
    list_filter = ('mensuality_date',)
    readonly_fields = ('current_streak', 'last_checkin', 'created_at')

    fieldsets = (
        ("Datos del Miembro", {
            "fields": ("name", "phone", "qr_code"),
        }),
        ("Mensualidad", {
            "fields": ("mensuality_date",),
        }),
        ("Racha (solo lectura)", {
            "fields": ("current_streak", "last_checkin", "created_at"),
        }),
    )

    @admin.display(description="Racha 🔥")
    def streak_badge(self, obj):
        streak = obj.current_streak
        if streak >= 30:
            color = "#cc0000"
        elif streak >= 10:
            color = "#ff6600"
        else:
            color = "#888"
        return format_html(
            '<span style="font-weight:700; color:{}; font-size:15px;">{} días</span>',
            color, streak
        )


@admin.register(Streaks)
class StreaksAdmin(ModelAdmin):
    list_display = ('nameStreak', 'daysStreak')
    search_fields = ('nameStreak',)
    ordering = ('daysStreak',)
