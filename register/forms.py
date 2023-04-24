from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from phonenumber_field.formfields import PhoneNumberField
from store.models import Customer

MITAA = (
    ('select', 'SELECT'),
    ('Juja', "JUJA"),
    ('Thika', "THIKA"),
    ('Rongai', "RONGAI"),
)

GENDER = (
    ('select', 'SELECT'),
    ('male','MALE'),
    ('female', 'FEMALE'),
    ('prefer not to say', 'PREFER NOT TO SAY'),
)


class CustomerForm(forms.ModelForm):
    # email = forms.EmailField(widget=forms.EmailInput())
    phone = PhoneNumberField(widget=forms.TextInput())
    location = forms.ChoiceField(choices=MITAA, widget=forms.Select())
    gender = forms.ChoiceField(choices=GENDER, widget=forms.Select())

    class Meta:
        model = Customer
        fields = ["phone", "location"]
        # fields = ["email", "phone", "location"]


class UserSignUpForm(UserCreationForm, CustomerForm):
    # email = forms.EmailField(max_length=254, required=True, help_text='Required', widget=forms.EmailInput())

    class Meta:
        model = User
        fields = ["username", "password1", "password2", "phone", "location", "gender"]
        # fields = ["username", "email", "password1", "password2", "phone", "location"]

    # def clean_email(self):
    #     email = self.cleaned_data['email']
    #     if User.objects.filter(email=email).exists():
    #         raise forms.ValidationError('Email is already taken')
    #     return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if Customer.objects.filter(phone=phone).exists():
            raise forms.ValidationError('Phone number is already taken')
        return phone

    def save(self, commit=True):
        user = super().save(commit=False)
        # user.email = self.cleaned_data['email']
        if commit:
            user.save()

        # Check if a Customer object already exists for the user
        try:
            customer = user.customer
        except Customer.DoesNotExist:
            customer = Customer(user=user)

        customer.phone = self.cleaned_data['phone']
        customer.location = self.cleaned_data['location']
        customer.gender = self.cleaned_data['gender']
        
        if commit:
            customer.save()

        return user


class ChangeUserDetailsForm(forms.ModelForm):
    phone = PhoneNumberField(widget=forms.TextInput())
    location = forms.ChoiceField(choices=MITAA, widget=forms.Select())

    class Meta:
        model = Customer
        fields = ["phone", "location"]

    def save(self, commit=True):
        customer = super().save(commit=False)
        customer.phone = self.cleaned_data['phone']
        customer.location = self.cleaned_data['location']
        if commit:
            customer.save()
        return customer
