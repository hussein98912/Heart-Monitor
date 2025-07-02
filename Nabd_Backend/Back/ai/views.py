from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse
import pandas as pd
from joblib import load
from patient.models import Patient_Signup


model = load(r'C:\Users\slman\Desktop\Nabd_Backend\Back\ai\random_forest_model_1.h5')
label_encoder = load(r'C:\Users\slman\Desktop\Nabd_Backend\Back\ai\label_encoder.pkl')

label_mapping = {
    'SR': 'Sinus Rhythm',
    'Afib': 'Atrial Fibrillation',
    'SB': 'Sinus Bradycardia',
    'SA': 'Sinoatrial Arrest or Sinus Arrest',
    'GSVT': 'General Supraventricular Tachycardia'
}

@api_view(['POST'])
def predict_view(request):
    try:
        patient_id = request.data.get('patient')
        print("Patient ID:", patient_id)  
        
        patient = get_object_or_404(Patient_Signup, id=patient_id)
        print("Patient Found:", patient) 
        
        input_data = pd.DataFrame([{
            'PatientAge': float(request.data.get('PatientAge')),
            'VentricularRate': float(request.data.get('ventricular_rate')),
            'AtrialRate': float(request.data.get('atrial_rate')),
            'QRSDuration': float(request.data.get('qrs_duration')),
            'QTInterval': float(request.data.get('qt_interval')),
            'QTCorrected': float(request.data.get('qt_corrected')),
            'RAxis': float(request.data.get('r_axis')),
            'TAxis': float(request.data.get('t_axis')),
            'QRSCount': int(request.data.get('qrs_count')),
            'TOffset': float(request.data.get('t_offset'))
        }])
        
        print("Input Data:", input_data)
        input_data = input_data.astype(float)
        predictions = model.predict(input_data)
        decoded_predictions = label_encoder.inverse_transform(predictions)
        prediction_result = decoded_predictions[0]
        
        print("Raw Predictions:", predictions)
        print("Decoded Predictions:", decoded_predictions)
        
        readable_prediction = label_mapping.get(prediction_result, prediction_result)
        
        print("Readable Prediction:", readable_prediction)
        return JsonResponse({'prediction': readable_prediction}, status=200)
    
    except Exception as e:
        print("Error:", e)
        return JsonResponse({'error': str(e)}, status=500)
