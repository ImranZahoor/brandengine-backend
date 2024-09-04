from rest_framework import serializers
from .models import Subscriber
from django.core.mail import send_mail

class SubcriberSerailizer(serializers.ModelSerializer):
    class Meta:
        model = Subscriber
        fields = (
            "email",
            "subscribe_at",
        )

    def validate_email(self, value):
        if Subscriber.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is already subscribed.")
        return value
    
    def create(self, validated_data):
        subscriber = Subscriber.objects.create(**validated_data)
        subject = "Subscription Confirmation"
        message = "Thank you for subscribing to our newsletter!"
        recipient_list = [subscriber.email]
        send_mail(
            subject,
            message,
            'brandsearchengine@gmail.com', 
            recipient_list,
            fail_silently=False,
        )

        return subscriber