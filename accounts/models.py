from django.db import models
from django.contrib.auth.models import User
from accounts.constants import GENDER_TYPE

# Create your models here.
class UserAccount(models.Model):
    user =models.OneToOneField(User,related_name="account",on_delete=models.CASCADE)
    account_no =models.IntegerField(unique = True)
    image = models.ImageField(upload_to="accounts/media/uploads/",blank=True,null=True)
    birth_date =models.DateField(null=True,blank =True)
    gender = models.CharField(max_length=10,choices =GENDER_TYPE)
    balance =models.DecimalField(default=0,max_digits =12,decimal_places =2)

    def __str__(self):
        return str(self.account_no)

class UserAddress(models.Model):
    user =models.OneToOneField(User,related_name="address",on_delete=models.CASCADE)
    street_address =models.CharField(max_length =100)
    city = models.CharField(max_length =100)
    postal_code =models.IntegerField()

    def __str__(self):
        return str(self.user.email)