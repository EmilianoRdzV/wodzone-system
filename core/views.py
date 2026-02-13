from datetime import timedelta, timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Member
from .models import Streaks
from django.shortcuts import render

def home(request):
    return render(request, 'index.html')

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

            #Hacemos el calculo para la fecha de vigencia de la mensualidad
            fechaMensualidad = member.mensuality_date
            nuevamensualidad = fechaMensualidad + timedelta(days=30) 


            # 🟢 Si fue exitoso
            return Response({
                "success": True,
                "message": msg,
                "name": member.name,
                "streakCurrent": member.current_streak,
                "streakName": nombre_racha,
                "expireDate":  nuevamensualidad,
            }, status=200)

        except Member.DoesNotExist:
            return Response({"error": "Miembro no encontrado"}, status=404)
        