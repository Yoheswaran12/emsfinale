from django import forms
from django.contrib.auth.models import User
from .models import Department, Position, EmployeeProfile, Attendance, Leave

class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['name']

class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['name', 'department']

class EmployeeCreateForm(forms.ModelForm):
    # User fields
    first_name = forms.CharField(max_length=150, required=True)
    last_name = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)

    # Profile fields
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    position = forms.ModelChoiceField(queryset=Position.objects.all(), required=False)
    phone = forms.CharField(max_length=20, required=False)
    photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
            EmployeeProfile.objects.create(
                user=user,
                department=self.cleaned_data.get('department'),
                position=self.cleaned_data.get('position'),
                phone=self.cleaned_data.get('phone'),
                photo=self.cleaned_data.get('photo'),
            )
        return user

class EmployeeUpdateForm(forms.ModelForm):
    # Profile fields
    department = forms.ModelChoiceField(queryset=Department.objects.all(), required=False)
    position = forms.ModelChoiceField(queryset=Position.objects.all(), required=False)
    phone = forms.CharField(max_length=20, required=False)
    photo = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class AttendanceForm(forms.ModelForm):
    class Meta:
        model = Attendance
        fields = ['employee', 'date', 'status', 'remarks']

class LeaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = ['start_date', 'end_date', 'reason']
        widgets = {
            'reason': forms.Textarea(attrs={'rows':3})
        }
