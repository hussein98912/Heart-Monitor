from django.db import models
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from datetime import datetime



#doctor register
class Signup(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE ,default='ukunown')
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.CharField(max_length=255, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    is_pending = models.BooleanField(default=True)
    certificate_image = models.ImageField(upload_to='doctor_images/', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])] , null=True, blank=True)
    identity_image = models.ImageField(upload_to='doctor_images/', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])] , null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.birthdate:
            today = datetime.today()
            self.age = today.year - self.birthdate.year - ((today.month, today.day) < (self.birthdate.month, self.birthdate.day))
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    def check_password(self, raw_password):
        """
        Check if the raw_password matches the stored hashed password.
        """
        return check_password(raw_password, self.password)
    



class DoctorProfile(models.Model):
    user = models.OneToOneField(Signup, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='doctor_images/', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])] , null=True, blank=True)

    def __str__(self):
        return f"Doctor Profile of {self.user.user.username}"