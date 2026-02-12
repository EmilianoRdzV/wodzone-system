from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Member

class CheckInView(APIView):
    def post(self, request):
        qr = request.data.get('qr_code')
        
        # Validar que enviaron algo
        if not qr:
            return Response({"error": "Falta código QR"}, status=400)

        try:
            # Buscar miembro
            member = Member.objects.get(qr_code=qr)
            
            # Ejecutar lógica de racha (del Sprint 2)
            success, msg = member.process_checkin()
            
            # Responder al escáner
            return Response({
                "success": success,
                "message": msg,
                "name": member.name,
                "streak": member.current_streak
            }, status=200)

        except Member.DoesNotExist:
            return Response({"error": "Miembro no encontrado"}, status=404)