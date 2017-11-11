from django import forms

from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email', 'class': 'form-signin-first'}))
    username = forms.CharField(max_length = 20, widget=forms.TextInput(attrs={'placeholder': 'Username', 'class': 'form-signin'}))
    firstname = forms.CharField(max_length = 50, widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-signin'}))
    lastname = forms.CharField(max_length = 50, widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-signin'}))
    password1 = forms.CharField(max_length = 200, 
                                label='Password', 
                                widget = forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-signin'}))
    password2 = forms.CharField(max_length = 200, 
                                label='Confirm password',  
                                widget = forms.PasswordInput(attrs={'placeholder': 'Repeat Password', 'class': 'form-signin'}))


    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username is already taken.")

        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
        return username

class ProfileForm(forms.Form):
    firstname = forms.CharField(max_length = 50, widget=forms.TextInput(attrs={'placeholder': 'First Name', 'class': 'form-signin'}))
    lastname = forms.CharField(max_length = 50, widget=forms.TextInput(attrs={'placeholder': 'Last Name', 'class': 'form-signin'}))
    age = forms.IntegerField(widget=forms.TextInput(attrs={'placeholder': 'Age', 'class': 'form-signin'}))
    bio = forms.CharField(max_length = 420, widget=forms.TextInput(attrs={'placeholder': 'Introduce yourself!', 'class': 'form-signin'}))
    image = forms.ImageField()

class ChangePasswordForm(forms.Form):
    password1 = forms.CharField(max_length = 200, 
                                label='Password', 
                                widget = forms.PasswordInput(attrs={'placeholder': 'Password', 'class': 'form-signin'}))
    password2 = forms.CharField(max_length = 200, 
                                label='Confirm password',  
                                widget = forms.PasswordInput(attrs={'placeholder': 'Repeat Password', 'class': 'form-signin'}))
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(ChangePasswordForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data

class CommentForm(forms.Form):
    comment = forms.CharField(max_length = 100)


