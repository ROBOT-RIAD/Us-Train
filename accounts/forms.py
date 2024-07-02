from django import forms
from .models import UserAccount,UserAddress
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .constants import GENDER_TYPE

class UserRegistrationForm(UserCreationForm):
    birth_date =forms .DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms .ChoiceField(choices =GENDER_TYPE)
    street_address =forms .CharField(max_length =100)
    city = forms .CharField(max_length =100)
    postal_code =forms .IntegerField()

    class Meta:
        model =User
        fields =['username','password1','password2','first_name','last_name','email','birth_date','gender','postal_code','city','street_address']

    def save(self, commit = True):
        our_user =super().save(commit=False)
        if commit == True:
            our_user.is_active = False
            our_user.save()
            birth_date = self.cleaned_data.get('birth_date')
            gender = self.cleaned_data.get('gender')
            street_address = self.cleaned_data.get('street_address')
            city = self.cleaned_data.get('city')
            postal_code = self.cleaned_data.get('postal_code')

            UserAddress.objects.create(
                user =our_user,
                postal_code=postal_code,
                city =city,
                street_address=street_address
            )
            UserAccount.objects.create(
                user =our_user,
                gender =gender,
                birth_date =birth_date,
                account_no =100000+our_user.id
            )
        return our_user
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class':(
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })


class EditeProfileForm(forms.ModelForm):
    birth_date =forms .DateField(widget=forms.DateInput(attrs={'type':'date'}))
    gender = forms .ChoiceField(choices =GENDER_TYPE)
    street_address =forms .CharField(max_length =100)
    city = forms .CharField(max_length =100)
    postal_code =forms .IntegerField()
    image = forms.ImageField(required=False)

    class Meta:
        model =User
        fields =['image','first_name','last_name','email','birth_date','gender','postal_code','city','street_address']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({
                'class': (
                    'appearance-none block w-full bg-gray-200 '
                    'text-gray-700 border border-gray-200 rounded '
                    'py-3 px-4 leading-tight focus:outline-none '
                    'focus:bg-white focus:border-gray-500'
                )
            })
        if self.instance:
            try:
                user_account =self.instance.account
                user_address =self.instance.address
            except UserAccount.DoesNotExist:
                user_account =None
                user_address =None
            if user_account:
                self.fields['image'].initial = user_account.image
                self.fields['gender'].initial = user_account.gender
                self.fields['birth_date'].initial = user_account.birth_date
                self.fields['street_address'].initial = user_address.street_address
                self.fields['city'].initial = user_address.city
                self.fields['postal_code'].initial = user_address.postal_code

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            user_account, created = UserAccount.objects.get_or_create(user=user)
            user_address, created = UserAddress.objects.get_or_create(user=user)

            user_account.image = self.cleaned_data['image']
            user_account.gender = self.cleaned_data['gender']
            user_account.birth_date = self.cleaned_data['birth_date']
            user_account.save()

            user_address.street_address = self.cleaned_data['street_address']
            user_address.city = self.cleaned_data['city']
            user_address.postal_code = self.cleaned_data['postal_code']
            user_address.save()
        return user




class AddMoneyForm(forms.ModelForm):

    class Meta:
        model = UserAccount
        fields =['balance']
    
    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account')
        super().__init__(*args, **kwargs)

    def clean_balance(self):
        min_dipo =100
        balance  = self.cleaned_data.get('balance')
        if balance < min_dipo :
            raise forms.ValidationError(
                f'You need to deposit at least {min_dipo} $'
            )
        return balance
    


