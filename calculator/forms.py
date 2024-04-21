# calculator/forms.py
from django import forms

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', )

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class CalculatorForm(forms.Form):
    weight = forms.FloatField(label='Weight in kg')
    height = forms.FloatField(label='Height in meters')
    age = forms.IntegerField(label='Age')
    gender = forms.ChoiceField(label='Gender', choices=[(1, 'Male'), (0, 'Female')])

# class WaterIntakeForm(forms.Form):
#     weight = forms.IntegerField(label='Your weight (in kg)')
#     activity_level = forms.ChoiceField(choices=[('low', 'Low'), ('medium', 'Medium'), ('high', 'High')], label='Activity Level')

class WaterIntakeForm(forms.Form):
    WEIGHT_CHOICES = [(i, str(i)) for i in range(30, 151)]  # Range from 30kg to 150kg
    ACTIVITY_LEVEL_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    CLIMATE_CHOICES = [
        ('cool', 'Cool'),
        ('moderate', 'Moderate'),
        ('hot', 'Hot'),
    ]
    
    weight = forms.ChoiceField(choices=WEIGHT_CHOICES, label="Weight (kg)")
    activity_level = forms.ChoiceField(choices=ACTIVITY_LEVEL_CHOICES, label="Activity Level")
    climate = forms.ChoiceField(choices=CLIMATE_CHOICES, label="Climate")

class ProductNameForm(forms.Form):
    product_name = forms.CharField(label='Enter Product Name', max_length=100, required=True)


class SleepForm(forms.Form):
    # Change the max_value to 12 to enforce standard 1-12 hour format for users
    hour = forms.IntegerField(label='Hour', min_value=1, max_value=12, required=True)
    minute = forms.IntegerField(label='Minute', min_value=0, max_value=59, required=True)
    # Add a choice field for AM/PM selection
    meridiem = forms.ChoiceField(choices=[('AM', 'AM'), ('PM', 'PM')], label='AM/PM', required=True)




