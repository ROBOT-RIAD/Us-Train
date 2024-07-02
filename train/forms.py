from django import forms
from .models import TicketBooking

class TicketBookingForm(forms.ModelForm):
    class Meta:
        model = TicketBooking
        fields = ['train_name', 'ticket_type', 'price', 'destination', 'coach', 'phone_no', 'sit_no','already_booking']

    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        self.fields['ticket_type'].disabled = True
        self.fields['ticket_type'].widget = forms.HiddenInput()
        self.fields['price'].disabled = True
        self.fields['price'].widget = forms.HiddenInput()
        self.fields['already_booking'].disabled = True
        self.fields['already_booking'].widget = forms.HiddenInput()
        
    

class RoyalTicketBookingForm(TicketBookingForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

class BuTicketBookingForm(TicketBookingForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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

class EconomyTicketBookingForm(TicketBookingForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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
