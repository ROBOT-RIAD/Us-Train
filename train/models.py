from django.db import models
from django.contrib.auth.models import User
from .constants import TICKET_TYPE, DISTINATION, TRAIN_NAME,COACH,SIT_NO

class TicketBooking(models.Model):
    user = models.ForeignKey(User, related_name="ticket", on_delete=models.CASCADE, default=None, null=True, blank=True)
    train_name = models.CharField(max_length=150, choices=TRAIN_NAME, default=None, null=True, blank=True)
    ticket_type = models.CharField(max_length=100, choices=TICKET_TYPE, default=None, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=12, decimal_places=2, default=None, null=True, blank=True)
    destination = models.CharField(max_length=200, choices=DISTINATION, default=None, null=True, blank=True)
    coach = models.IntegerField(choices=COACH,default=None, null=True, blank=True)
    phone_no = models.CharField(max_length=12, default=None, null=True, blank=True)
    sit_no = models.IntegerField(choices=SIT_NO,default=None, null=True, blank=True)
    trip_no = models.IntegerField(default=1000001)
    already_booking = models.BooleanField(null=True, blank=True)
    finish_trip = models.BooleanField(default=False)

    class Meta:
        ordering = ['time']