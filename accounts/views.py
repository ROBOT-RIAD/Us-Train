from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views.generic import FormView
from .forms import UserRegistrationForm,EditeProfileForm,AddMoneyForm
from django.urls import reverse_lazy
from django.contrib.auth import login,logout
from django.contrib.auth.views import LoginView,LogoutView
from django.contrib import messages
from django.views import View
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin

from  django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes

# Create your views here.

def send_transaction_email(user,amount,subject,template):
    message = render_to_string(template,{'user': user,'amount':amount })
    send_email =EmailMultiAlternatives(subject,"",to =[user.email])
    send_email.attach_alternative(message,"text/html")
    send_email.send()

class UserRegistrationView(FormView):
    template_name ='accounts/user_registration.html'
    form_class =UserRegistrationForm
    success_url =reverse_lazy("login")

    def form_valid(self, form):
        user=form.save()
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        confirm_link =f"http://127.0.0.1:8000/accounts/active/{uid}/{token}"
        email_subject = "Confirm your Email"
        email_body =render_to_string('accounts/confirm_email.html',{'confirm_link':confirm_link})
        email = EmailMultiAlternatives(email_subject,"",to =[user.email])
        email.attach_alternative(email_body,'text/html')
        email.send()
        messages.success(self.request, 'account create Successfully,verify email check email')
        return super().form_valid(form)
    
def Activate(request,uid64,token):
    try:
        uid =urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user =None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active =True
        user.save()
        return redirect('login')
    else:
        return redirect('register')

class UserLoginView(LoginView):
    template_name ='accounts/user_login.html'
    def get_success_url(self):
        return reverse_lazy('home')
    def form_valid(self,form):
        messages.success(self.request,"Login successfully")
        return super().form_valid(form)
    

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')
    
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            if request.user.is_authenticated:
                logout(self.request)
            return redirect(self.next_page)
        else:
            return super().dispatch(request, *args, **kwargs)
        



class UserAccountUpdateView(LoginRequiredMixin,View):
    template_name = 'accounts/profile.html'
    def get(self, request):
        form =EditeProfileForm(instance=request.user)
        return render(request, self.template_name, {'form': form})
    
    def post(self, request):
        form = EditeProfileForm(request.POST,request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
        return render(request, self.template_name, {'form': form})
    



class AddMoneyView(LoginRequiredMixin,FormView):
    template_name = 'accounts/deposit.html'
    form_class = AddMoneyForm
    success_url = reverse_lazy('home')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['account'] = self.request.user.account
        return kwargs

    def form_valid(self, form):
        account = self.request.user.account
        balance =form.cleaned_data['balance']
        account.balance += balance
        messages.success(self.request,'your deposit was successfully checked your email')
        send_transaction_email(self.request.user,balance,"deposit",'accounts/depo_email.html')
        account.save()
        return super().form_valid(form)