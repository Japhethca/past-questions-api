from django import forms
from core.models import User, Review


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=300, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)


class SignupForm(forms.Form):
    full_name = forms.CharField(max_length=30, strip=True)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput, required=True)

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')

        if password != confirm_password:
            msg = 'password must match'
            self.add_error('password', msg)
            self.add_error('confirm_password', msg)
        return confirm_password

    def clean_email(self):
        email = self.cleaned_data.get('email')

        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        else:
            raise forms.ValidationError('Email already exist')

    def clean(self):
        fullname = str(self.cleaned_data.get('full_name')).split(' ')

        if len(fullname) < 2:
            self.add_error('full_name', 'This is field must contain firstname and lastname')
        else:
            self.cleaned_data['first_name'] = fullname[0]
            self.cleaned_data['last_name'] = fullname[1]
            self.cleaned_data.pop('full_name')
        self.cleaned_data.pop('confirm_password')


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('comment', )
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3})
        }
