from django.contrib.auth.forms import UserCreationForm #import the form
from django.contrib.auth.models import User #import the model
class UserSignUpForm(UserCreationForm):
    class Meta:
        fields = ('username', 'password1', 'password2',
                  'email',)# 'favourite_colour',)
        model = User
#Change how it is displayed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = "Your Name"
        self.fields['email'].label = "Email Address"
        #self.fields['favourite_colour'].label = "Favorite Colour"
