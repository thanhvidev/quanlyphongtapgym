from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import CustomUser


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text='Required.')

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'phonenumber',
                  'gender', 'age', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('Địa chỉ Email đã tồn tại')
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if len(first_name) < 2:
            raise forms.ValidationError('Tên phải có ít nhất 2 ký tự.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if len(last_name) < 2:
            raise forms.ValidationError('Họ phải có ít nhất 2 ký tự.')
        return last_name

    def clean_phonenumber(self):
        phonenumber = self.cleaned_data.get('phonenumber')
        if len(phonenumber) != 10:
            raise forms.ValidationError(
                'Số điện thoại phải có 10 chữ số.')
        return phonenumber

    def clean_age(self):
        age = self.cleaned_data.get('age')
        if age < 0 or age > 100:
            raise forms.ValidationError('Tuổi phải lớn hơn 0.')
        return age

    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        return gender

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                'Mật khẩu và mật khẩu nhập lại không giống nhau.')
        return password2

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if len(password1) < 8:
            raise forms.ValidationError('Mật khẩu phải dài ít nhất 8 ký tự.')
        if not any(char.isdigit() for char in password1):
            raise forms.ValidationError(
                'Mật khẩu phải chứa ít nhất một chữ số.')
        return password1


class LoginForm(forms.Form):
    email = forms.CharField(label='Email')
    password = forms.CharField(label='Mật khẩu', widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            validate_email(email)
        except ValidationError:
            raise forms.ValidationError('Vui lòng nhập đúng định dạng email.')
        return email


class AvatarUploadForm(forms.Form):
    avatar = forms.ImageField(label='Chọn ảnh đại diện')
