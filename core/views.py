from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Member
from .models import Streaks
from datetime import timedelta
from django.utils import timezone
from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

def calculaMensualidad(member):
    hoy = timezone.now().date()
    fmensualidad = member

    if not fmensualidad:
        return hoy

    diferencia = hoy - fmensualidad
    if diferencia.days > 31:
        return hoy
 
    nmensualidad = fmensualidad + timedelta(days=31)
    return nmensualidad

def muestraInfo(request, qr):
    member = Member.objects.get(qr_code=qr)
    expdate = calculaMensualidad(member.mensuality_date)
    return render(request, 'index.html', {'member': member, 'fechaexp': expdate})


class CheckInView(APIView):
    def post(self, request):
        qr = request.data.get('qr_code')
        
        if not qr:
            return Response({"error": "Falta código QR"}, status=400)

        try:
            member = Member.objects.get(qr_code=qr)

            success, msg = member.process_checkin()

            # 🔴 Si no fue exitoso (ya vino hoy)
            if not success:
                return Response({
                    "success": False,
                    "error": msg,
                    "name": member.name,
                    "streak": member.current_streak
                }, status=400)
            
            #Validamos si coincide coan alguna racha existente
            nombre_racha = "No cumple con ninguna racha"
            streakNow = Streaks.objects.filter(daysStreak=member.current_streak).first()
            if streakNow: 
                    nombre_racha = streakNow.nameStreak

            #muestraInfo(request, qr)

            # 🟢 Si fue exitoso
            return Response({
                "success": True,
                "message": msg,
                "name": member.name,
                "streakCurrent": member.current_streak,
                "streakName": nombre_racha,
            }, status=200)

        except Member.DoesNotExist:
            return Response({"error": "Miembro no encontrado"}, status=404)
        