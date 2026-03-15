from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models import Email
from .serializers import EmailSerializer
from ..encryption import encrypt_message
from django.contrib.auth.models import User

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def inbox_api(request):
    emails = Email.objects.filter(recipient=request.user).order_by('-timestamp')
    serializer = EmailSerializer(emails, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def sent_api(request):
    emails = Email.objects.filter(sender=request.user).order_by('-timestamp')
    serializer = EmailSerializer(emails, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def compose_api(request):
    data = request.data
    try:
        recipient = User.objects.get(username=data.get('recipient'))
    except User.DoesNotExist:
        return Response({"error": "Recipient does not exist."}, status=400)

    subject_enc = encrypt_message(data.get('subject'))
    body_enc = encrypt_message(data.get('body'))

    Email.objects.create(
        sender=request.user,
        recipient=recipient,
        subject=subject_enc,
        body_encrypted=body_enc
    )
    return Response({"success": "Email sent!"})
