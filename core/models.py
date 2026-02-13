from django.db import models
from django.utils import timezone
from datetime import timedelta

class Member(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre Completo")
    phone = models.CharField(max_length=20, verbose_name="Teléfono")
    qr_code = models.CharField(max_length=50, unique=True, verbose_name="Código QR")
    
    # Datos de la Racha
    current_streak = models.IntegerField(default=0, verbose_name="Racha Actual")
    last_checkin = models.DateTimeField(null=True, blank=True, verbose_name="Última Visita")

    #fecha de mensualidad
    mensuality_date = models.DateField(null=True, blank=True, verbose_name="Mensualidad")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.current_streak} días)"

    def process_checkin(self):
        now = timezone.localtime(timezone.now())  # fecha y hora locales
        today = now.date()  # solo para comparar fechas si quieres

        # Evitar doble check-in usando solo fecha
        if self.last_checkin and self.last_checkin.date() == today:
            return False, "Ya registraste visita hoy"

        # Calcular el día anterior esperado
        weekday = today.weekday()
        days_back = 3 if weekday == 0 else 1
        expected_prev = today - timedelta(days=days_back)

        # Evaluar racha
        if self.last_checkin and self.last_checkin.date() == expected_prev:
            self.current_streak += 1
        else:
            self.current_streak = 1  # rompe racha

        # Guardar fecha y hora reales
        self.last_checkin = now
        self.save()

        return True, "Check-in Exitoso"
    
class Streaks(models.Model):
    nameStreak = models.CharField(max_length=100, verbose_name="Nombre Racha")
    daysStreak = models.IntegerField(default=0, verbose_name="Dias totales")

    def __str__(self):
        return f"{self.nameStreak} ({self.daysStreak} días)"
    
