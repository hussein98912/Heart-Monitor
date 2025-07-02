from django.urls import path
from .views import get_patient_signup, update_patient_signup , signup_view, login_view , logout_view , get_prediction_view, ECGReadingDetailAPIView,send_ecg_to_doctor
from . import views
from .views import patientListAPIView

urlpatterns = [
    path('patient-signup/', signup_view),
    path('patient-login/', login_view, name='login'),
    path('patient-logout/', logout_view, name='logout'),
    path('patient-signup/<int:user_id>/', get_patient_signup),
    path('patient-profile/<int:user_id>/update/', update_patient_signup, name= 'patient-profile'),
    path('medical-data/', views.post_medical_data, name='medical_data'),
    path('patient/<int:patient_id>/result/', get_prediction_view, name='get_prediction_view'),
    path('ecg-readings/<int:pk>/', ECGReadingDetailAPIView.as_view(), name='ecg-reading-detail'),
    path('send-ecg/<int:patient_id>/', send_ecg_to_doctor, name='send-ecg-to-doctor'),
    path('patients/', patientListAPIView.as_view(), name='patient-list'),

]
