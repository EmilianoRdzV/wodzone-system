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

    #fechas de mensualidad
    mensuality_date = models.DateField(null=True, blank=True, verbose_name="Mensualidad")
    
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.current_streak} días)"

    def process_checkin(self):
        now = timezone.localtime(timezone.now())  # fecha y hora locales
        today = now.date()  # solo para comparar fechas si quieres

        #SI EL ULTIMO CHECK ES EN VIERNES Y REGISTRA EL LUNES LA RACHA SIGUE
        #SI PASAN MAS DE 3 DIAS LA RACHA SE ROMPE SOLO PARA FINES DE SEMANA
        #ENTRE SEMANA SOLO PERMITE FALTAR 1 DIA, SI PASAN MAS DE DOS SE REINICIA.

        diff = (today - self.last_checkin.date()).days
        last_day = self.last_checkin.weekday()

        weekend_case = last_day == 4 and diff <= 3
        weekday_case = diff <= 2

        if weekend_case or weekday_case:
            self.current_streak += 1
        else:
            self.current_streak = 1

        # Guardar fecha y hora reales
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
    
