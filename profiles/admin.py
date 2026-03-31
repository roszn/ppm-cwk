from django.contrib import admin
from django import forms
from .models import EmployeeProfile
from accounts.models import CustomUser

class EmployeeProfileAdminForm(forms.ModelForm):
    user_email = forms.EmailField(label='User Email')
    line_manager_email = forms.EmailField(label='Line Manager Email', required=False)
    date_of_birth = forms.DateField(label='Date of Birth', input_formats=['%d/%m/%Y'], widget=forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': 'DD/MM/YYYY'}), required=False)

    class Meta:
        model = EmployeeProfile
        fields = '__all__'
        exclude = ['user', 'line_manager']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['user_email'].initial = self.instance.user.email
            if self.instance.line_manager:
                self.fields['line_manager_email'].initial = self.instance.line_manager.email

    def clean_user_email(self):
        email = self.cleaned_data['user_email']
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise forms.ValidationError(f'No user found with email: {email}')

    def clean_line_manager_email(self):
        email = self.cleaned_data.get('line_manager_email')
        if not email:
            return None
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise forms.ValidationError(f'No user found with email: {email}')

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.user = self.cleaned_data['user_email']
        instance.line_manager = self.cleaned_data['line_manager_email']
        if commit:
            instance.save()
        return instance

@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    form = EmployeeProfileAdminForm
    list_display = ['user', 'job_role', 'department', 'line_manager']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'job_role', 'department']
    list_filter = ['department']
