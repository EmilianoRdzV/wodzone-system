import uuid
from django.db import models
from django.utils import timezone
from datetime import timedelta


def _generate_qr():
    return f"WZ-{uuid.uuid4().hex[:8].upper()}"


class Member(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre Completo")
    phone = models.CharField(max_length=20, verbose_name="Teléfono")
    qr_code = models.CharField(
        max_length=50, unique=True, verbose_name="Código QR",
        blank=True, help_text="Se genera automáticamente si se deja vacío (ej: WZ-A1B2C3D4)"
    )
    
    # Datos de la Racha
    current_streak = models.IntegerField(default=0, verbose_name="Racha Actual")
    last_checkin = models.DateTimeField(null=True, blank=True, verbose_name="Última Visita")

    #fechas de mensualidad
    mensuality_date = models.DateField(null=True, blank=True, verbose_name="Mensualidad")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.current_streak} días)"

    def save(self, *args, **kwargs):
        if not self.qr_code:
            self.qr_code = _generate_qr()
        super().save(*args, **kwargs)

    def process_checkin(self):
        now = timezone.localtime(timezone.now())
        today = now.date()

        if self.last_checkin is None:
            # Primer check-in del miembro
            self.current_streak = 1

        else:
            diff = (today - self.last_checkin.date()).days

            if diff == 0:
                # Ya hizo check-in hoy — no suma, solo confirma entrada
                return False, "Ya registraste tu entrada hoy"

            last_day = self.last_checkin.weekday()

            # Viernes (4) → el fin de semana no cuenta, permite hasta lunes (3 días)
            # Entre semana → permite 1 día de falta, si pasan 2+ se reinicia
            weekend_case = last_day == 4 and diff <= 3
            weekday_case = diff <= 2

            if weekend_case or weekday_case:
                self.current_streak += 1
            else:
                self.current_streak = 1

        self.last_checkin = now
        self.save()
        return True, "Check-in Exitoso"
    
    def saveNDateM(self, m):
        self.mensuality_date = m
        self.save()
        
    
class Streaks(models.Model):
    nameStreak = models.CharField(max_length=100, verbose_name="Nombre Racha")
    daysStreak = models.IntegerField(default=0, verbose_name="Dias totales")

    def __str__(self):
        return f"{self.nameStreak} ({self.daysStreak} días)"
    
