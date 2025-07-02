from rest_framework import serializers
from .models import Signup , DoctorProfile
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    class Meta:
        model = User
        fields = ['id','username', 'password', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}  


class SignupSerializer(serializers.ModelSerializer):
    certificate_image = serializers.FileField(required=False)
    identity_image = serializers.FileField(required=False)
    user = UserSerializer()


    class Meta:
        model = Signup
        fields = ['user','gender','birthdate','address' , 'certificate_image', 'identity_image','phone_number']



from rest_framework import serializers
from .models import DoctorProfile

class DoctorProfileSerializer(serializers.ModelSerializer):
    user = SignupSerializer()

    class Meta:
        model = DoctorProfile
        fields = ['user','profile_image']


   
from rest_framework import serializers
from django.contrib.auth.models import User

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance


class DoctorListSerializer(serializers.ModelSerializer):
     first_name = serializers.CharField(source='user.user.first_name', read_only=True)
     last_name = serializers.CharField(source='user.user.last_name', read_only=True)
     phone_number = serializers.CharField(source='user.phone_number', read_only=True)
     email = serializers.CharField(source='user.user.email', read_only=True)
     address = serializers.CharField(source='user.address', read_only=True)

     class Meta:
        model = DoctorProfile
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'address']

