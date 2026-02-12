from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Member

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

            # 🟢 Si fue exitoso
            return Response({
                "success": True,
                "message": msg,
                "name": member.name,
                "streak": member.current_streak
            }, status=200)

        except Member.DoesNotExist:
            return Response({"error": "Miembro no encontrado"}, status=404)
