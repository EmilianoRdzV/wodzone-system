from django.db import models
from django.utils import timezone
from datetime import timedelta

class Member(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre Completo")
    phone = models.CharField(max_length=20, verbose_name="Teléfono")
    qr_code = models.CharField(max_length=50, unique=True, verbose_name="Código QR")
    
    # Datos de la Racha
    current_streak = models.IntegerField(default=0, verbose_name="Racha Actual")
    last_checkin = models.DateField(null=True, blank=True, verbose_name="Última Visita")

    #fecha de mensualidad
    mensuality_date = models.DateField(null=True, blank=True, verbose_name="Mensualidad")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.current_streak} días)"

    def process_checkin(self):
        """
        Calcula si la racha continúa o se rompe.
        Ignora Sábados (5) y Domingos (6).
        """
        today = timezone.localdate()
        
        # 1. Evitar doble check-in
        if self.last_checkin == today:
            return False, "Ya registraste visita hoy"

        # 2. Calcular el día anterior esperado
        # Si es Lunes (0), debió venir el Viernes (3 días atrás)
        # Si es cualquier otro día, debió venir ayer (1 día atrás)
        weekday = today.weekday()
        days_back = 3 if weekday == 0 else 1
        expected_prev = today - timedelta(days=days_back)

        # 3. Evaluar Racha
        maintained = False
        # Si vino el día esperado O si es su primera vez
        if self.last_checkin == expected_prev or self.last_checkin is None:
            self.current_streak += 1
            maintained = True
        else:
            # Rompió la racha, reinicia a 1 (hoy cuenta)
            self.current_streak = 1 

        # 4. Guardar
        self.last_checkin = today
        self.save()

        return True, "Check-in Exitoso"
    
class Streaks(models.Model):
    nameStreak = models.CharField(max_length=100, verbose_name="Nombre Racha")
    daysStreak = models.IntegerField(default=0, verbose_name="Dias totales")

    def __str__(self):
        return f"{self.nameStreak} ({self.daysStreak} días)"
    
