from django.core.validators import RegexValidator
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Now we are creting a Registerform
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, label="Email Address")
    username = forms.CharField(required=True, label="Username")

    # Only letters and hyphens
    name_validator = RegexValidator(
        regex=r'^[a-zA-Z-]+$', 
        message='Only letters and hyphens are allowed.'
    )

    first_name = forms.CharField(
        required=True,
        min_length=3,
        max_length=50,
        validators=[name_validator],
        label="First Name",
        # optional 
        widget=forms.TextInput(attrs={'placeholder': 'Enter first name', 'id': 'first_name_input'})
    )

    last_name = forms.CharField(
        required=True,
        min_length=3,
        max_length=50,
        validators=[name_validator],
        label="Last Name"
    )

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    # ---------------------------
    # Field cleaning methods
    # ---------------------------
    def clean_first_name(self):
        return self.cleaned_data['first_name'].title()

    def clean_last_name(self):
        return self.cleaned_data['last_name'].title()

    def clean_username(self):
        return self.cleaned_data['username'].lower()

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email is already registered.")
        return email
    # ........................................
    # ........................................

# Note each form should have it's own class 
class PostForm(forms.ModelForm):
    pass
