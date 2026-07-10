
################ FORMS FOR USER INPUT ####################
   ######## COLLECTS AND VALIDATES USER INPUT ############


# Imports Djangoos form system
from django import forms
# Import models from models.py, models become the foundation for the forms
from .models import Post, Profile, Relationship


# A ModelForm automatically creates a form based on a model.
    # The Meta class tells Django how to build the form.
    # only fields and labels will appear on the webpage
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'image']
        labels = {'description': 'What would you like to say?'}

# ProfileForm, this form edits a users profile
    # fields and labels are displayed on the profile page
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name','email', 'dob', 'bio']
        labels = {'first_name':'First Name',
                    'last_name': 'Last Name',
                    'email': 'Email',
                    'dob':'Date of Birth',
                    'bio':'Bio'}


# RelationshipForm, this form works with friends requests
    # fields = __all__ , means show every field in the model
        # sender, receiver and status displayed on Friend requests page
        # sender will be displayed as 'Accept friend request form:'
class RelationshipForm(forms.ModelForm):
    class Meta:
        model = Relationship
        fields = '__all__'
        labels = {
        'sender': 'Accept friend request from:',
        'receiver':'Send friend request to:',
        'status': 'Current status:'
        }



