from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from datetime import datetime
from django.core.exceptions import ValidationError
from django.db import IntegrityError
import re
from .models import Patient_Signup , PatientMedicalData,ECGReading
from django.contrib.auth.models import User
from .serializers import SignupSerializer  , PatientMedicalDataSerializer,ECGReadingSerializer , PatientListSerializer
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from rest_framework import generics
from doctor.models import DoctorProfile


@api_view(['POST'])
def signup_view(request):
    if request.method == 'POST':
        gender = request.data.get('gender')
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        address = request.data.get('address')
        birthdate_str = request.data.get('birthdate')
        phone_number=request.data.get('phone_number')

        if not re.match(r"^\d{10}$", phone_number):
            return Response({'error': 'Phone number must be exactly 10 digits.'}, status=status.HTTP_400_BAD_REQUEST)

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

        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return Response({'error': 'Invalid email address format.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.create_user(username=username, email=email, password=password,
                                             first_name=first_name, last_name=last_name)
        except IntegrityError:
            return Response({'error': 'Username or email already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            signup = Patient_Signup.objects.create(user=user, gender=gender, address=address, birthdate=birthdate, age=age,phone_number=phone_number)
        except ValidationError as e:
            return Response({'error': e.message}, status=status.HTTP_400_BAD_REQUEST)
        serializer = SignupSerializer(signup)
        return Response({'message': 'Signup successful.', 'data': serializer.data}, status=status.HTTP_201_CREATED)
    




@api_view(['POST'])
def login_view(request):
    if request.method == 'POST':
        # Extract username and password from request data
        username = request.data.get('username')
        password = request.data.get('password')
        
        if not username or not password:
            return Response({'status': 'error', 'message': 'Username and password are required'}, status=400)
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if user is not None:
            # Authentication successful
            # Generate or retrieve token
            token, created = Token.objects.get_or_create(user=user)
            return Response({'status': 'success', 'token': token.key})
        else:
            # Authentication failed
            return Response({'status': 'error', 'message': 'Invalid credentials'}, status=400)





@api_view(['POST'])
def post_medical_data(request):
    serializer = PatientMedicalDataSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









        





from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Patient_Signup
from .serializers import SignupSerializer

@api_view(['GET'])
def get_patient_signup(request, user_id):
    try:
        patient_signup = Patient_Signup.objects.get(user_id=user_id)
        serializer = SignupSerializer(patient_signup)
        return Response(serializer.data)
    except Patient_Signup.DoesNotExist:
        return Response({'error': 'Patient signup does not exist'}, status=404)


@api_view(['PUT'])
def update_patient_signup(request, user_id):
    try:
        patient_signup = Patient_Signup.objects.get(user_id=user_id)
    except Patient_Signup.DoesNotExist:
        return Response({'error': 'Patient signup does not exist'}, status=status.HTTP_404_NOT_FOUND)

    serializer = SignupSerializer(patient_signup, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'Information has been updated successfully'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





@api_view(['GET', 'PUT'])
def doctor_view_patients(request):
    if request.method == 'GET':
        # Retrieve all patients
        patients = Patient_Signup.objects.all()
        serializer = SignupSerializer(patients, many=True)
        return Response(serializer.data)

    elif request.method == 'PUT':
        # Extract patient ID and doctor ID from request data
        patient_id = request.data.get('patient_id')
        doctor_id = request.data.get('doctor_id')

        # Validate patient and doctor IDs
        try:
            patient = Patient_Signup.objects.get(pk=patient_id)
        except Patient_Signup.DoesNotExist:
            return Response({'error': 'Patient not found'}, status=status.HTTP_404_NOT_FOUND)

        # Here you can add additional validation for doctor ID if needed

        # Update the patient's doctor attribute
        patient.doctor_id = doctor_id
        patient.save()

        # Serialize and return updated patient data
        serializer = SignupSerializer(patient)
        return Response(serializer.data)
 

    


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




@api_view(['GET'])
def get_prediction_view(request, patient_id):
    try:
        # Get the patient
        patient = get_object_or_404(Patient_Signup, id=patient_id)
        
        # Get the patient's medical data
        medical_data = PatientMedicalData.objects.filter(patient=patient).first()
        
        if not medical_data:
            return Response({'error': 'No medical data found for this patient.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Serialize the medical data
        serializer = PatientMedicalDataSerializer(medical_data)
        
        # Return the serialized data
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    


class ECGReadingDetailAPIView(generics.RetrieveAPIView):
    queryset = ECGReading.objects.all()
    serializer_class = ECGReadingSerializer




@api_view(['GET'])
def send_ecg_to_doctor(request, patient_id):
    try:
        ecg_reading = ECGReading.objects.get(patient_id=patient_id)
    except ECGReading.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = ECGReadingSerializer(ecg_reading)
    return Response(serializer.data)


class patientListAPIView(generics.ListAPIView):
    queryset = Patient_Signup.objects.all()
    serializer_class = PatientListSerializer
 