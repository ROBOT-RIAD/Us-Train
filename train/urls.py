from django.urls import path
from train.views import RoyalTicketView,BusinessTicketView,EconomyTicketView,RoyalTicketSitView,BusinessTicketSitView,EconomyTicketSitView

urlpatterns = [
    path('Royal-view/',RoyalTicketSitView.as_view(),name='royal'),  
    path('Business-view/',BusinessTicketSitView.as_view(),name='business'), 
    path('Economy-view/',EconomyTicketSitView.as_view(),name='economy'),

    





    path('Royal-ticket/',RoyalTicketView.as_view(),name='royal_ticket'),  
    path('Business-ticket/',BusinessTicketView.as_view(),name='business_ticket'), 
    path('Economy-ticket/',EconomyTicketView.as_view(),name='economy_ticket'),
]