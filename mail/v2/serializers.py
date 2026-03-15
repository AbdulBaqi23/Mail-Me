from rest_framework import serializers
from ..models import Email
from ..encryption import decrypt_message

class EmailSerializer(serializers.ModelSerializer):
    subject = serializers.SerializerMethodField()
    body = serializers.SerializerMethodField()
    sender = serializers.StringRelatedField()
    recipient = serializers.StringRelatedField()

    class Meta:
        model = Email
        fields = ['id', 'sender', 'recipient', 'subject', 'body', 'timestamp']

    def get_subject(self, obj):
        return decrypt_message(obj.subject)

    def get_body(self, obj):
        return decrypt_message(obj.body_encrypted)
