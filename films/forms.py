from django.contrib.auth.forms import UserCreationForm
from films.models import User
from django import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]
        
    
class RatingForm(forms.Form):
    name = forms.CharField(max_length=100)
    review = forms.CharField(widget=forms.Textarea)
    RATING_CHOICES = [
        (5, '5 stars'),
        (4, '4 stars'),
        (3, '3 stars'),
        (2, '2 stars'),
        (1, '1 star'),
    ]
    rating = forms.ChoiceField(choices=RATING_CHOICES, widget=forms.RadioSelect)