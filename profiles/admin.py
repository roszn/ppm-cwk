from django.contrib import admin
from django import forms
from .models import EmployeeProfile
from accounts.models import CustomUser


class EmployeeProfileAdminForm(forms.ModelForm):
    user_email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='First Name', required=False)
    last_name = forms.CharField(label='Last Name', required=False)
    new_password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput(render_value=False),
        required=False,
    )
    confirm_password = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(render_value=False),
        required=False,
    )
    line_manager_email = forms.EmailField(label='Line Manager Email', required=False)
    date_of_birth = forms.DateField(
        label='Date of Birth',
        input_formats=['%d/%m/%Y'],
        widget=forms.DateInput(format='%d/%m/%Y', attrs={'placeholder': 'DD/MM/YYYY'}),
        required=False,
    )

    class Meta:
        model = EmployeeProfile
        fields = '__all__'
        exclude = ['user', 'line_manager']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['user_email'].initial = self.instance.user.email
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['new_password'].help_text = 'Leave blank to keep the current password.'
            if self.instance.line_manager:
                self.fields['line_manager_email'].initial = self.instance.line_manager.email
        else:
            self.fields['first_name'].required = True
            self.fields['last_name'].required = True
            self.fields['new_password'].required = True
            self.fields['confirm_password'].required = True

    def clean_user_email(self):
        email = self.cleaned_data['user_email']
        if self.instance.pk:
            try:
                return CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                raise forms.ValidationError(f'No user found with email: {email}')
        else:
            if CustomUser.objects.filter(email=email).exists():
                raise forms.ValidationError('A user with this email already exists.')
            return email

    def clean_line_manager_email(self):
        email = self.cleaned_data.get('line_manager_email')
        if not email:
            return None
        try:
            return CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            raise forms.ValidationError(f'No user found with email: {email}')

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('new_password')
        confirm = cleaned_data.get('confirm_password')
        if password or confirm:
            if password != confirm:
                self.add_error('confirm_password', 'Passwords do not match.')
        return cleaned_data

    def save(self, commit=True):
        # Build an unsaved instance carrying the profile field values from the form
        form_instance = super().save(commit=False)

        if self.instance.pk:
            # Edit mode: update the existing user account
            user = self.cleaned_data['user_email']
            user.first_name = self.cleaned_data.get('first_name') or user.first_name
            user.last_name = self.cleaned_data.get('last_name') or user.last_name
            password = self.cleaned_data.get('new_password')
            if password:
                user.set_password(password)
            user.save()
            form_instance.user = user
            form_instance.line_manager = self.cleaned_data['line_manager_email']
            if commit:
                form_instance.save()
            return form_instance
        else:
            # Add mode: create the user — the post_save signal auto-creates a blank profile
            email = self.cleaned_data['user_email']
            base_username = email.split('@')[0]
            username = base_username
            counter = 1
            while CustomUser.objects.filter(username=username).exists():
                username = f'{base_username}{counter}'
                counter += 1
            user = CustomUser.objects.create_user(
                username=username,
                email=email,
                password=self.cleaned_data['new_password'],
                first_name=self.cleaned_data.get('first_name', ''),
                last_name=self.cleaned_data.get('last_name', ''),
            )
            # Fetch the profile the signal just created and populate it with form data
            profile = EmployeeProfile.objects.get(user=user)
            for field in [
                'profile_picture', 'job_role', 'department', 'description', 'about_me',
                'salary', 'phone_number', 'address', 'date_of_birth',
                'emergency_contact_name', 'emergency_contact_phone',
            ]:
                setattr(profile, field, getattr(form_instance, field))
            profile.line_manager = self.cleaned_data['line_manager_email']
            if commit:
                profile.save()
            return profile


@admin.register(EmployeeProfile)
class EmployeeProfileAdmin(admin.ModelAdmin):
    form = EmployeeProfileAdminForm
    list_display = ['user', 'job_role', 'department', 'line_manager']
    search_fields = ['user__email', 'user__first_name', 'user__last_name', 'job_role', 'department']
    list_filter = ['department']
