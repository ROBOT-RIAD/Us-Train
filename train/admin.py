from django.contrib import admin
from .models import TicketBooking
from django.db.models import Max
from django.contrib.auth.models import User
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

def send_transaction_email(users, subject, template):
    for user in users:
        message = render_to_string(template, {'user': user})
        send_email = EmailMultiAlternatives(subject, "", to=[user.email])
        send_email.attach_alternative(message, "text/html")
        send_email.send()

@admin.register(TicketBooking)
class TicketBookingAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        
        max_trip_no = TicketBooking.objects.aggregate(Max('trip_no'))['trip_no__max']
        if obj.finish_trip and max_trip_no:
            max_trip_users = TicketBooking.objects.filter(trip_no=max_trip_no)
            
            if max_trip_users.exists():
                users = User.objects.filter(id__in=max_trip_users.values_list('user_id', flat=True))
                send_transaction_email(users, 'Trip Completed', 'complate_email.html')
                max_trip_users.update(finish_trip=True)
                new_trip = TicketBooking(
                    trip_no=max_trip_no + 1,
                    finish_trip=False
                )
                new_trip.save()
