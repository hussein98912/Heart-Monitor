from django.urls import path
from .views import signup_view, login_view
from .views import UserCreateAPIView, logout_view
from .views import doctor_profile , update_doctor_profile , update_user ,DoctorListAPIView
from patient.views import  doctor_view_patients

urlpatterns = [
    path('doctor-signup/', signup_view, name='signup'),
    path('doctor-login/', login_view, name='login'),
    path('doctor-logout/', logout_view, name='logout'),
    path('user/create/', UserCreateAPIView.as_view(), name='user-create'),
    path('doctor/profile/<int:pk>/', doctor_profile, name='doctor_profile'),
    path('doctor/update/<int:pk>/', update_doctor_profile, name='update_doctor_profile'),
    path('update_personal_info/<int:pk>/', update_user, name='update_personal_info'),
    path('patients/doctor/', doctor_view_patients, name='update_patient_doctor'),
    path('doctors/', DoctorListAPIView.as_view(), name='doctor-list'),
    
]
