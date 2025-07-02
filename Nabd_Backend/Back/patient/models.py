from django.db import models
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from datetime import datetime
from doctor.models import  DoctorProfile
from django.contrib.postgres.fields import ArrayField




class Patient_Signup(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE ,default='ukunown')
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    address = models.CharField(max_length=255, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='doctor_images/', validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])] , null=True, blank=True)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE ,null=True,blank=True)
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




class PatientMedicalData(models.Model):
    patient = models.ForeignKey(Patient_Signup, on_delete=models.CASCADE, related_name='medical_data')
    ventricular_rate = models.FloatField(null=True, blank=True)
    atrial_rate = models.FloatField(null=True, blank=True)
    qrs_duration = models.FloatField(null=True, blank=True)
    qt_interval = models.FloatField(null=True, blank=True)
    qt_corrected = models.FloatField(null=True, blank=True)
    r_axis = models.FloatField(null=True, blank=True)
    t_axis = models.FloatField(null=True, blank=True)
    qrs_count = models.IntegerField(null=True, blank=True)
    t_offset = models.FloatField(null=True, blank=True)
    prediction = models.CharField(max_length=255, null=True, blank=True)  

    def __str__(self):
        return f"Medical data for {self.patient.user.first_name} {self.patient.user.last_name}"


class ECGReading(models.Model):
    patient = models.OneToOneField(Patient_Signup, on_delete=models.CASCADE)
    timestamp = models.DateTimeField()
    values = ArrayField(models.FloatField(), size=1000,null=True)


    class Meta:
        indexes = [
            models.Index(fields=['patient', 'timestamp']),
        ]

    def __str__(self):
        return f"{self.patient.name} - {self.timestamp} - Value: {self.value}"