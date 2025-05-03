from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
import random
import uuid

# Create your models here.


def generate_wallet_id():
    
    _id = str(random.randrange(0000000,9999999))
    
    if len(_id) == 7:
        if Wallet.objects.filter(wallet_id=_id).exists():
            _id = str(random.randrange(0000000,9999999))
            if len(_id) == 7:
                _id = _id
            else:
                pass
        else:
            _id = _id
    else:
        _id = str(random.randrange(0000000,9999999))
        if len(_id) == 7:
            if Wallet.objects.filter(wallet_id=_id):
                _id = str(random.randrange(0000000,9999999))
                if len(_id) == 7:
                    _id = _id
                else:
                    pass
            else:
                _id = _id
    return _id 


TransactionType = [
    ('ADD MONEY', 'ADD MONEY'),
    ('WITHDRAW', 'WITHDRAW'),
    ('TRANSFER', 'TRANSFER'),
    ('PURCHASED', 'PURCHASED'),
]


Status = [
    ('SUCCESSFUL', 'SUCCESSFUL'),
    ('PENDING', 'PENDING'),
    ('FAILED', 'FAILED'),
]


class Appointment(models.Model):
    doctor = models.ForeignKey('accounts.DoctorsProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='doctor_appointment')
    patient = models.ForeignKey('accounts.PatientProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name='patient_appointment')
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField(null=True, blank=True)
    outcome = models.TextField(null=True, blank=True)
    held = models.BooleanField()
    rescheduled = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
     
    
    def __str__(self):
        return f"{self.doctor}'s appointment with {self.patient}"
    
    
class Messages(models.Model):
    pass



class Wallet(models.Model):
    user = models.OneToOneField('accounts.CustomUser', on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    wallet_id = models.CharField(_("wallet id"), max_length=7, validators=[MinLengthValidator(7), MaxLengthValidator(7)], default=generate_wallet_id, unique=True)
    password = models.CharField(_("password"), max_length=225)
    is_disabled = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user}'s wallet"
    