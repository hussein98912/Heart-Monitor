from django.contrib import admin
from .models import Patient_Signup, ECGReading, PatientMedicalData


class PatientSignupAdmin(admin.ModelAdmin):
    list_display = ['user_display', 'gender', 'address', 'birthdate', 'age']
    search_fields = ['user__username', 'address']

    def user_display(self, obj):
        return obj.user.username
    user_display.short_description = 'Username'

admin.site.register(Patient_Signup, PatientSignupAdmin)


class ECGReadingAdmin(admin.ModelAdmin):
    list_display = ('patient_display', 'timestamp', 'get_values')
    list_filter = ('patient', 'timestamp')
    search_fields = ('patient__user__username',)

    def get_values(self, obj):
        return obj.value[:10]  # Display the first 10 values as an example
    get_values.short_description = 'ECG Values'

    def patient_display(self, obj):
        return obj.patient.user.username
    patient_display.short_description = 'Patient Username'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(ECGReading, ECGReadingAdmin)


class PatientMedicalDataAdmin(admin.ModelAdmin):
    list_display = [
        'patient_display', 'ventricular_rate', 'atrial_rate', 'qrs_duration', 'qt_interval',
        'qt_corrected', 'r_axis', 't_axis', 'qrs_count', 't_offset', 'prediction'
    ]
    search_fields = ['patient__user__username', 'prediction']
    list_filter = ['patient', 'ventricular_rate', 'atrial_rate']

    def patient_display(self, obj):
        return obj.patient.user.username
    patient_display.short_description = 'Patient Username'

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

admin.site.register(PatientMedicalData, PatientMedicalDataAdmin)
