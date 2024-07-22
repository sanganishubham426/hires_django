from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser
import datetime


class RecruiterModel(models.Model):
    class Meta:
        db_table = 'recruiter_user_tb'
    recruiter_user_id = models.CharField(default="None", max_length=60, primary_key=True)
    recruiter_user_firstname = models.CharField(max_length = 30, default="None", blank=True, null=True)
    recruiter_user_lastname = models.CharField(max_length = 30, default="None", blank=True, null=True)
    recruiter_user_mobileno = models.CharField(max_length = 15, default="None", blank=True, null=True)
    recruiter_user_email = models.CharField(max_length = 100, default="None", blank=True, null=True)
    recruiter_user_password = models.CharField(max_length = 100, default="None", blank=True, null=True)
    recruiter_user_is_action = models.BooleanField(default=True)
    recruiter_user_is_verified = models.BooleanField(default=False)
    recruiter_user_is_loggedin = models.BooleanField(default=False)
    recruiter_user_registration_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.recruiter_user_firstname + " " + self.recruiter_user_lastname



class RecruiterEmailVerification(models.Model):
    
    class Meta:
        db_table = "recruiter_email_verification"

    recruiter_user = models.OneToOneField(RecruiterModel, on_delete=models.CASCADE, primary_key=True)
    OTP_verify = models.CharField(max_length = 10, blank=False, null=False)
    expire_time = models.DateTimeField(default= datetime.datetime.now())
    user_registration_date = models.DateTimeField(auto_now_add=True)

