from django.contrib.auth import authenticate
from django.http import JsonResponse
from rest_framework.decorators import api_view 
from rest_framework.authtoken.models import Token
from .serializers import SignupSerializer , DoctorProfileSerializer , UserUpdateSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from .models import Signup , DoctorProfile
from .serializers import SignupSerializer , DoctorListSerializer
from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import re
from rest_framework import generics

@api_view(['POST'])
def signup_view(request):
    if request.method == 'POST':
        # Extract data from request
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        address = request.data.get('address')
        birthdate_str = request.data.get('birthdate')
        gender = request.data.get('gender')
        phone_number=request.data.get('phone_number')

        if not re.match(r"^\d{10}$", phone_number):
                return Response({'error': 'Phone number must be exactly 10 digits.'}, status=status.HTTP_400_BAD_REQUEST)

        if len(password) < 8:
            return Response({'error': 'Password must be at least 8 characters long.'}, status=status.HTTP_400_BAD_REQUEST)
        if not any(char.isupper() for char in password):
            return Response({'error': 'Password must contain at least one uppercase letter.'}, status=status.HTTP_400_BAD_REQUEST)
        if not any(char.islower() for char in password):
            return Response({'error': 'Password must contain at least one lowercase letter.'}, status=status.HTTP_400_BAD_REQUEST)
        if not any(char.isdigit() for char in password):
            return Response({'error': 'Password must contain at least one digit.'}, status=status.HTTP_400_BAD_REQUEST)
        if not any(char in "!@#$%^&*()-_+=<>?/" for char in password):
            return Response({'error': 'Password must contain at least one special character.'}, status=status.HTTP_400_BAD_REQUEST)

        birthdate = None
        if birthdate_str:
            try:
                birthdate = datetime.strptime(birthdate_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({'error': 'Invalid birthdate format. Use YYYY-MM-DD.'}, status=status.HTTP_400_BAD_REQUEST)

        age = None
        if birthdate:
            today = datetime.today().date()
            age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
            if age < 18:
                return Response({'error': 'You must be at least 18 years old to register.'}, status=status.HTTP_400_BAD_REQUEST)

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return Response({'error': 'Invalid email address format.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create Django User
        try:
            user = User.objects.create_user(username=username, email=email, password=password,
                                             first_name=first_name, last_name=last_name)
        except IntegrityError:
            return Response({'error': 'Username or email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Create Signup entry
        try:
            signup = Signup.objects.create(user=user, gender=gender, address=address, birthdate=birthdate, age=age)
        except ValidationError as e:
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
        doctor_profile = DoctorProfile.objects.create(user=signup )
        serializer = SignupSerializer(signup)

        return Response({'message': 'Signup successful.', 'data': serializer.data}, status=status.HTTP_201_CREATED)



@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            try:
                signup = Signup.objects.get(user=user)
                if signup.is_pending:
                    return Response({'error': 'Doctor account is pending approval. Please contact admin.'}, status=403)
            except Signup.DoesNotExist:
                return Response({'error': 'Signup information not found. Please contact admin.'}, status=404)

            
            token, created = Token.objects.get_or_create(user=user)
            return Response({'token': token.key})
        else:
            
            return Response({'error': 'Invalid credentials'}, status=400)


from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from .serializers import UserSerializer

class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer





@api_view(['GET'])
def doctor_profile(request, pk):
    try:
        doctor_profile = DoctorProfile.objects.get(pk=pk)
    except DoctorProfile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = DoctorProfileSerializer(doctor_profile)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = DoctorProfileSerializer(doctor_profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['PUT'])
def update_doctor_profile(request, pk):
    try:
        doctor_profile = DoctorProfile.objects.get(pk=pk)
    except DoctorProfile.DoesNotExist:
        return Response({'error': 'Doctor profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == 'PUT':
        # Update DoctorProfile fields
        serializer = DoctorProfileSerializer(doctor_profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()

            # Update related User instance
            user_data = request.data.get('user', {})
            user_instance = doctor_profile.user
            user = user_instance.user  # Access the related User instance
            user_serializer = UserSerializer(user, data=user_data, partial=True)  # Use UserSerializer to update user fields
            if user_serializer.is_valid():
                user_serializer.save()
                return Response({'message': 'Doctor profile image updated successfully.'})   
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        # Get the token from the request's authorization header
        token = request.auth

        if token:
            # Delete the token to log the user out
            token.delete()
            return Response({'message': 'Logout successful.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Token not provided or invalid.'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PUT'])
def update_user(request, pk):
    try:
        user = User.objects.get(pk=pk)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PUT':
        serializer = UserUpdateSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Doctor information updated successfully.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

 
 
class DoctorListAPIView(generics.ListAPIView):
    queryset = DoctorProfile.objects.all()
    serializer_class = DoctorListSerializer
 
 
 
 
 
 
 

 
 
 