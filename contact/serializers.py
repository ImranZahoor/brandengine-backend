from rest_framework import serializers
from contact.models import Contact
from django.core.mail import send_mail


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = '__all__'
        
    def create(self, validated_data):
        contacter = Contact.objects.create(**validated_data)
        subject = "We have received your details."
        message = "Thank you for sending us your details. We will get back to you shortly."
        recipient_list = [contacter.email]
        send_mail(
            subject,
            message,
            'brandsearchengine@gmail.com', 
            recipient_list,
            fail_silently=False,
        )

        return contacter