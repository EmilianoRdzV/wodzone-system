from datetime import timedelta

from django.utils import timezone
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Member, Streaks


def home(request):
    return render(request, 'index.html')


def _calcular_mensualidad(mensualidad, member):
    hoy = timezone.now().date()
    diff = (hoy - mensualidad).days

    if diff >= 31:
        nueva = hoy
        member.saveNDateM(nueva)
        return nueva

    return mensualidad + timedelta(days=31)


def _buscar_racha(days: int) -> str:
    streak = Streaks.objects.filter(daysStreak=days).first()
    return streak.nameStreak if streak else ""


class CheckInView(APIView):
    def post(self, request):
        qr = request.data.get('qr_code')

        if not qr:
            return Response({"error": "Falta código QR"}, status=400)

        try:
            member = Member.objects.get(qr_code=qr)
        except Member.DoesNotExist:
            return Response({"error": "Miembro no encontrado"}, status=404)

        success, msg = member.process_checkin()

        if not success:
            return Response({
                "success": False,
                "error": msg,
                "name": member.name,
                "streakCurrent": member.current_streak,
            }, status=400)

        streak_name = _buscar_racha(member.current_streak) or "No cumple con ninguna racha"
        expiry = _calcular_mensualidad(member.mensuality_date, member)

        return Response({
            "success": True,
            "message": msg,
            "name": member.name,
            "streakCurrent": member.current_streak,
            "streakName": streak_name,
            "expiryDate": expiry.strftime("%d / %b / %Y").upper(),
        }, status=200)


class MemberInfoView(APIView):
    def get(self, request, qr):
        try:
            member = Member.objects.get(qr_code=qr)
        except Member.DoesNotExist:
            return Response({"error": "Miembro no encontrado"}, status=404)

        streak_name = _buscar_racha(member.current_streak) or "No cumple con ninguna racha"
        expiry = _calcular_mensualidad(member.mensuality_date, member)

        return Response({
            "success": True,
            "name": member.name,
            "streakCurrent": member.current_streak,
            "streakName": streak_name,
            "expiryDate": expiry.strftime("%d / %b / %Y").upper(),
        })
