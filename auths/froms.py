from django import forms
from users.models import CustomUser
from apis.models import News365


class RegisterFrom(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','username','email','password']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Email'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Password'}),
        }
        help_texts = {
            'username': '',  # Username এর নিচের বড় লেখা বন্ধ করে দিচ্ছি
        }


class LoginForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username','password']
        widgets = {
                                   
            'username': forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Username'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder': 'Password'}),
        }
        help_texts = {
            'username': '',  # Username এর নিচের বড় লেখা বন্ধ করে দিচ্ছি
        }



class NewsCreateForm(forms.ModelForm):
    class Meta:
        model = News365
        fields = ['category', 'head_lines', 'discriptions','image1', 'image2','image3','video','adverticement','is_impotent']
        widgets = {
         
            'category': forms.Select(attrs={
                'class': 'form-control mb-3',
            }),
            'head_lines': forms.TextInput(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Enter headline'
            }),
            'discriptions': forms.Textarea(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Write your description',
                'rows': 4
            }),
            'image1': forms.ClearableFileInput(attrs={
                'class': 'form-control mb-3',
            }),
            'image2': forms.ClearableFileInput(attrs={
                'class': 'form-control mb-3',
            }),
            'image3': forms.ClearableFileInput(attrs={
                'class': 'form-control mb-3',
            }),
            'video': forms.Textarea(attrs={
                'class': 'form-control mb-3',
                'placeholder': 'video embuder',
                'rows': 4
            }),
            'adverticement': forms.ClearableFileInput(attrs={
                'class': 'form-control mb-3',
            }),
            'is_impotent': forms.CheckboxInput(attrs={
                'class': 'form-check-input',
            }),
        }
 