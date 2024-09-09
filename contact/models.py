from django.db import models
from django.core.validators import RegexValidator


# Create your models here.
class Contact(models.Model):
    name=models.CharField(max_length=100)
    email=models.EmailField()
    phone_regex = RegexValidator(
    regex=r"^\+?1?\d{9,15}$",
    message=(
        "Phone number must be entered in the format: '+999999999'. "
        "Up to 15 digits allowed."
        ),
    )
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)
    subject=models.CharField(max_length=150)
    message=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name