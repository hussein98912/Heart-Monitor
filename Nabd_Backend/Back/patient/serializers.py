from rest_framework import serializers
from .models import Patient_Signup, ECGReading
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}} 

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class SignupSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient_Signup
        fields = ['user', 'gender', 'address', 'birthdate', 'age', 'image', 'doctor','phone_number']


    def update(self, instance, validated_data):
        user_data = validated_data.pop('user', {})
        user_instance = instance.user

        # Update the user instance
        for attr, value in user_data.items():
            if attr == 'password' and value:
                user_instance.set_password(value)
            else:
                setattr(user_instance, attr, value)
        user_instance.save()

        # Update the Patient_Signup instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance



    def to_representation(self, instance):
        representation = super().to_representation(instance)
        user_data = representation.pop('user')
        representation.update(user_data)
        return representation
    




from rest_framework import serializers
from .models import PatientMedicalData

class PatientMedicalDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientMedicalData
        fields = [
            'id', 
            'patient', 
            'ventricular_rate', 
            'atrial_rate', 
            'qrs_duration', 
            'qt_interval', 
            'qt_corrected', 
            'r_axis', 
            't_axis', 
            'qrs_count', 
            't_offset', 
            'prediction'
        ]
        read_only_fields = ['prediction']



class ECGReadingSerializer(serializers.ModelSerializer):
    patient = SignupSerializer()

    class Meta:
        model = ECGReading
        fields = ['id', 'patient', 'timestamp', 'value']




class PatientListSerializer(serializers.ModelSerializer):
     id = serializers.IntegerField(source='user.id', read_only=True)
     first_name = serializers.CharField(source='user.user.first_name', read_only=True)
     last_name = serializers.CharField(source='user.user.last_name', read_only=True)
     phone_number = serializers.CharField(source='user.phone_number', read_only=True)
     email = serializers.CharField(source='user.user.email', read_only=True)
     address = serializers.CharField(source='user.address', read_only=True)

     class Meta:
        model = Patient_Signup
        fields = ['id','first_name', 'last_name', 'phone_number', 'email', 'address']
