from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import  FormView,ListView
from django.contrib import messages
from .forms import RoyalTicketBookingForm, BuTicketBookingForm, EconomyTicketBookingForm
from .models import TicketBooking
from accounts.models import UserAccount
from django.db.models import Max
from django.contrib.auth.mixins import LoginRequiredMixin


from  django.core.mail import EmailMessage,EmailMultiAlternatives
from django.template.loader import render_to_string
def send_transaction_email(ticket_booking, subject, template):
    message = render_to_string(template, {'ticket_booking': ticket_booking})
    send_email = EmailMultiAlternatives(subject, "", to=[ticket_booking.user.email])
    send_email.attach_alternative(message, "text/html")
    send_email.send()



class TicketBookingMixin(LoginRequiredMixin,FormView):
    model = TicketBooking
    def get_form_kwargs(self): 
        kwargs = super().get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_initial(self):
        initial = super().get_initial()
        initial.update({'user': self.request.user})
        return initial
    def form_valid(self, form):
        user_account = UserAccount.objects.get(user=self.request.user)
        ticket_booking = form.save(commit=False)
        ticket_booking.user = self.request.user
        max_trip_no = TicketBooking.objects.aggregate(Max('trip_no'))['trip_no__max']
        print(max_trip_no)

        if TicketBooking.objects.filter(coach=ticket_booking.coach, sit_no=ticket_booking.sit_no,trip_no=max_trip_no, already_booking=True).exists():
            messages.error(self.request, f"Seat {ticket_booking.sit_no} is already booked.")
            return self.form_invalid(form)

        if user_account.balance >= ticket_booking.price:
            user_account.balance -= ticket_booking.price
            user_account.save()
            ticket_booking.trip_no = max_trip_no
            ticket_booking.save()
            self.send_confirmation_email(ticket_booking)
            messages.success(self.request, "Ticket booked successfully!")
            return super().form_valid(form)
        else:
            messages.error(self.request, "Your account does not have enough balance to book this ticket.")
            return self.form_invalid(form)
        
    def send_confirmation_email(self, ticket_booking):
        subject = "Ticket Booking Confirmation"
        template = 'buy_ticket_email.html'
        send_transaction_email(ticket_booking, subject, template)

class RoyalTicketView(TicketBookingMixin):
    form_class = RoyalTicketBookingForm
    template_name = 'royal_ticket_booking.html'
    success_url = reverse_lazy('royal')

    def get_initial(self):
        initial = super().get_initial()
        initial.update({'ticket_type': 'Royal', 'price': 800,'already_booking': True})
        return initial

class BusinessTicketView(TicketBookingMixin):
    form_class = BuTicketBookingForm
    template_name = 'business_ticket_booking.html'
    success_url = reverse_lazy('business')

    def get_initial(self):
        initial = super().get_initial()
        initial.update({'ticket_type': 'Business', 'price': 700,'already_booking': True})
        return initial

class EconomyTicketView(TicketBookingMixin):
    form_class = EconomyTicketBookingForm
    template_name = 'economy_ticket_booking.html'
    success_url = reverse_lazy('economy')

    def get_initial(self):
        initial = super().get_initial()
        initial.update({'ticket_type': 'Economy', 'price': 500,'already_booking': True})
        return initial
    



class BaseTicketSitView(LoginRequiredMixin,ListView):
    model = TicketBooking
    context_object_name = 'tickets'

    def get_queryset(self):
        ticket_type = self.ticket_type
        trip_no = self.trip_no
        queryset = TicketBooking.objects.all()

        if  trip_no is not None:
            queryset = queryset.filter(trip_no=trip_no)

        if ticket_type is not None:
            queryset = queryset.filter(ticket_type=ticket_type)

        return queryset
    
class RoyalTicketSitView(BaseTicketSitView):
    template_name = 'royal_ticket.html'
    ticket_type = 'Royal'
    trip_no = None

    def dispatch(self, *args, **kwargs):
        if self.trip_no is None:
            self.trip_no = TicketBooking.objects.aggregate(Max('trip_no'))['trip_no__max']
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tickets = self.get_queryset()
        booked_seats = {
            1: [ticket.sit_no for ticket in tickets if ticket.coach == 1],
            2: [ticket.sit_no for ticket in tickets if ticket.coach == 2],
        }
        context['booked_seats'] = booked_seats
        # max_trip_no = tickets.aggregate(models.Max('trip_no'))['trip_no__max']
        # print(max_trip_no)
        return context
    

class BusinessTicketSitView(BaseTicketSitView):
    template_name = 'business_ticket.html'
    ticket_type = 'Business'
    trip_no = None

    def dispatch(self, *args, **kwargs):
        if self.trip_no is None:
            self.trip_no = TicketBooking.objects.aggregate(Max('trip_no'))['trip_no__max']
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(ticket_type=self.ticket_type)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tickets = self.get_queryset()
        booked_seats = {
            3: [ticket.sit_no for ticket in tickets if ticket.coach == 3],
            4: [ticket.sit_no for ticket in tickets if ticket.coach == 4],
        }
        context['booked_seats'] = booked_seats
        return context
    

class EconomyTicketSitView(BaseTicketSitView):
    template_name = 'economy_ticket.html'
    ticket_type = 'Economy'
    trip_no = None

    def dispatch(self, *args, **kwargs):
        if self.trip_no is None:
            self.trip_no = TicketBooking.objects.aggregate(Max('trip_no'))['trip_no__max']
        return super().dispatch(*args, **kwargs)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tickets = self.get_queryset()
        booked_seats = {
            5: [ticket.sit_no for ticket in tickets if ticket.coach == 5],
            6: [ticket.sit_no for ticket in tickets if ticket.coach == 6],
        }
        context['booked_seats'] = booked_seats
        return context