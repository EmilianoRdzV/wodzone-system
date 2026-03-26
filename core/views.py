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

def calculaMensualidad(mensualidad, qr):
    member = Member.objects.get(qr_code=qr)
    hoy = timezone.now().date()
    nmensualidad = None

    #PREMISAS
    #LA MENSUALIDAD SE COBRA POR 31 DIAS(MES)
    #EL BOX ABRE 6 DIAS A LA SEMANA
    #DIAS HABILIDES DE ENTRENAMIENTO 24

    diffMensualidad = hoy - mensualidad

    if diffMensualidad.days >= 31:
        nmensualidad = hoy
        member.saveNDateM(nmensualidad)

    if diffMensualidad.days < 31: 
        nmensualidad = mensualidad + timedelta(days=31)

    return nmensualidad

def buscaRacha(dStreak):
    dayS = Streaks.objects.filter(daysStreak=dStreak).first()
    if dayS:
        return dayS.nameStreak
    else:
        return ""
    return nStreak

def muestraInfo(request, qr):
    member = Member.objects.get(qr_code=qr)
    expdate = calculaMensualidad(member.mensuality_date, member.qr_code)
    streak = buscaRacha(member.current_streak)
    showModal = True
    if streak is None or streak == "": showModal = False
    return render(request, 'index.html', {'member': member, 'fechaexp': expdate, 'streak': streak, 'showmodal': showModal})


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
        