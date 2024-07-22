from rest_framework import serializers
from .models import RecruiterModel

from django.contrib.auth.hashers import make_password, check_password
import re

import string
import random
from datetime import datetime
'''
    Serializer is used to convert json into django supported complex objects
'''
class UserSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RecruiterModel   # Model
        fields = "__all__"  # Consider all fields

        #fields = ['user_id', 'name', 'roll', 'city']
        #exclude = ["title"]

    def validate(self, data):

        recruiter_user_firstname = data["recruiter_user_firstname"]
        recruiter_user_lastname = data["recruiter_user_lastname"]
        recruiter_user_email = data["recruiter_user_email"]
        recruiter_user_password = data["recruiter_user_password"]
        # recruiter_user_mobileno = data["recruiter_user_mobileno"]

        # Password Patterns
        Passwordpattern = re.compile("^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$")
        email_pattern = re.compile("^[a-zA-Z][\w\.-]*@[\w\.-]+\.\w+$")
        # mobile_pattern = r'^\+966\d{9}$'

        # Validation 
        if len(recruiter_user_firstname) <= 2:
            raise serializers.ValidationError({'errorMsg':'Length of first Name should be more than 2'})
        if not recruiter_user_firstname.isalpha():
            raise serializers.ValidationError({'errorMsg':'First Name is required'})
    
        if len(recruiter_user_lastname) <= 2:
            raise serializers.ValidationError({'errorMsg':'Length of last Name should be more than 2'})
        if not recruiter_user_lastname.isalpha():
            raise serializers.ValidationError({'errorMsg':'Last Name is required'})

        if RecruiterModel.objects.filter(recruiter_user_email=recruiter_user_email).exists():
            raise serializers.ValidationError({'errorMsg': 'Email is already existed'})
        # if recruiter_user_email.find("@gmail.com") == -1:
        #     raise serializers.ValidationError({'errorMsg': 'Only Gmail is acceptable'})
        if not recruiter_user_email:
             raise serializers.ValidationError({'errorMsg':'Email is required'})
        if not re.search(email_pattern, recruiter_user_email):
            raise serializers.ValidationError({"errorMsg":'Invalid email address'})
        
        # if not re.match(mobile_pattern, recruiter_user_mobileno):
        #     raise serializers.ValidationError({"message": "Invalid phone number", "code": 400, "status": "error"})

        if len(recruiter_user_password) <= 7:
            raise serializers.ValidationError({'errorMsg':'Length of password should be between 8 and 18'})

        if not re.search(Passwordpattern, recruiter_user_password):
            raise serializers.ValidationError({'errorMsg':'Password should contain uppercase, lowercase, numbers and special characters'})
     
        # Salt string for security
        randomstr = ''.join(random.choices(string.ascii_letters +
                             string.digits, k=10))

        # Encrypt password with argon2 algorithms
        data["recruiter_user_password"] = make_password(recruiter_user_password,salt=randomstr, hasher='argon2')
        

        return data

# class EmailSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = RecruiterModel
#         fields = ['recruiter_user_id']

    
#     def validate(self, data):

#         recruiter_user_id = data["recruiter_user_id"]
       
#         if RecruiterModel.objects.filter(recruiter_user_id=recruiter_user_id).exists():
            
#             user = RecruiterModel.objects.get(recruiter_user_id=recruiter_user_id)
#             if user.recruiter_user_is_verified:
#                 raise serializers.ValidationError({'errorMsg': 'Account is already verified'})
                
#         else:    
#             raise serializers.ValidationError({'errorMsg': 'Email does not existed'})
        
#         return data

class LoginSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RecruiterModel
        fields = ['recruiter_user_email', 'recruiter_user_password']

    
    def validate(self, data):

        recruiter_user_email = data["recruiter_user_email"]
        pwd = data["recruiter_user_password"]
       
        if RecruiterModel.objects.filter(recruiter_user_email=recruiter_user_email).exists():
            
            user = RecruiterModel.objects.get(recruiter_user_email=recruiter_user_email)

            if not user.recruiter_user_is_verified:
                raise serializers.ValidationError({'errorMsg': 'Account is not verified',"recruiter_user_id":user.recruiter_user_id})
            # elif not user.user_is_recruiter:
            #     raise serializers.ValidationError({'errorMsg': 'User is not a recruiter'})
            else:

                # if not user.recruiter_user_is_loggedin:
                check_pwd = check_password(pwd, user.recruiter_user_password)
                if check_pwd:
                
                    user.recruiter_user_is_loggedin = True
                    user.last_login = datetime.now()
                    user.save()

                    
                else:    
                    raise serializers.ValidationError({'errorMsg': "Wrong credentials","recruiter_user_id":""})
                # else:
                #     raise serializers.ValidationError({'errorMsg': "Already logged in", 'user_is_recruiter': user.user_is_recruiter})
        else:    
            raise serializers.ValidationError({'errorMsg': 'Invalid Email',"recruiter_user_id":""})

        

        return data

class ChangePasswordSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RecruiterModel
        fields = ['recruiter_user_email','recruiter_user_password']

    def validate(self, data):

        pwd = data["recruiter_user_password"]
        recruiter_user_email = data["recruiter_user_email"]

        if RecruiterModel.objects.filter(recruiter_user_email=recruiter_user_email).exists():
            
            user = RecruiterModel.objects.get(recruiter_user_email=recruiter_user_email)
            
            if not user.recruiter_user_is_verified:
                raise serializers.ValidationError({'errorMsg': 'Account is not verified'})
            else:

                if user.recruiter_user_is_action:
                    if user.recruiter_user_is_loggedin:
                        check_pwd = check_password(pwd, user.recruiter_user_password)
                        
                        if check_pwd:
                            return data
                        else:
                            raise serializers.ValidationError({'errorMsg': 'old password is wrong'})
                    else:
                        raise serializers.ValidationError({'errorMsg': 'You are not loggedin'})
                else:
                    raise serializers.ValidationError({'errorMsg': 'Your account is not activated'})
        else:    
            raise serializers.ValidationError({'errorMsg': 'Wrong credentials'})


# class UserEditProfileSerializer(serializers.ModelSerializer):

#     class Meta:

#         model = RecruiterModel
#         fields = ["user_birthdate","user_mobileno","user_gender", "user_summary", "user_address","user_jobtitle", "user_country", "user_pincode", "user_facebook", "user_linkedin", "user_github", "user_medium", "user_other1", "user_other2", "user_stackoverflow", "user_address"]


#     def validate(self, data):

#         user_birthdate = data["user_birthdate"]
#         user_mobileno = data["user_mobileno"]
#         user_gender =  data["user_gender"]
#         user_summary = data["user_summary"]
#         user_address = data["user_address"]
#         user_jobtitle = data["user_jobtitle"]
#         user_country = data["user_country"]
#         user_pincode = data["user_pincode"]
#         user_facebook = data["user_facebook"]
#         user_linkedin = data["user_linkedin"]
#         user_github = data["user_github"]
#         user_medium = data["user_medium"]
#         user_other1 = data["user_other1"]
#         user_other2 = data["user_other2"]
#         user_stackoverflow = data["user_stackoverflow"]

#         mobile_number_pattern = re.compile("^\+?\d{1,3}?[-.\s]?\d{9,12}$")
#         facebook_pattern = re.compile("^https?:\/\/(?:www\.)?facebook\.com\/[a-zA-Z0-9_\.]+\/?$")
#         linkedin_pattern = re.compile("^https?:\/\/(?:www\.)?linkedin\.com\/[a-zA-Z0-9_\/-]+\/?$")
#         github_pattern = re.compile("^https?:\/\/(?:www\.)?github\.com\/[a-zA-Z0-9_\-]+\/?$")
#         medium_pattern = re.compile("^https?:\/\/(?:www\.)?medium\.com\/@?[a-zA-Z0-9_\-]+\/?$")
#         stackoverflow_pattern = re.compile("^https?:\/\/(?:www\.)?stackoverflow\.com\/[a-zA-Z0-9_\/-]+\/?$")
#         link_pattern = re.compile(
#                             "^(?:http|ftp)s?://"  # scheme
#                             "(?:[a-zA-Z0-9-]{1,63}\.)+[a-zA-Z]{2,63}"  # domain name
#                             "(?:/[-a-zA-Z0-9_.,;:|+&@#%*()=!/?]*)?$"  # path and query string
#                         )



#         if len(user_mobileno) > 0:
#             if not re.search(mobile_number_pattern, user_mobileno):
#                 raise serializers.ValidationError({'errorMsg':'Invalid Mobile no.'})

#         if len(user_facebook) > 0:
#             if not re.search(facebook_pattern, user_facebook):
#                 raise serializers.ValidationError({'errorMsg':'Invalid facebbok link'})


#         if len(user_linkedin) > 0:
#             if not re.search(linkedin_pattern, user_linkedin):
#                 raise serializers.ValidationError({'errorMsg':'Invalid linkedIn link'})

        
#         if len(user_github) > 0:
#             if not re.search(github_pattern, user_github):
#                 raise serializers.ValidationError({'errorMsg':'Invalid github link'})
            

#         if len(user_medium) > 0:
#             if not re.search(medium_pattern, user_medium):
#                 raise serializers.ValidationError({'errorMsg':'Invalid medium link'})

#         if len(user_other1) > 0:
#             if not re.search(link_pattern, user_other1):
#                 raise serializers.ValidationError({'errorMsg':'Invalid  link website 1'})


#         if len(user_other2) > 0:
#             if not re.search(link_pattern, user_other2):
#                 raise serializers.ValidationError({'errorMsg':'Invalid  link website 2'})

        
#         if len(user_stackoverflow) > 0:
#             if not re.search(stackoverflow_pattern, user_stackoverflow):
#                 raise serializers.ValidationError({'errorMsg':'Invalid stackoverflow link'})
        
#         return data
    


class UserEditProfileSerializer(serializers.ModelSerializer):

    class Meta:

        model = RecruiterModel
        fields = ["recruiter_user_mobileno"]


    def validate(self, data):

        recruiter_user_mobileno = data["recruiter_user_mobileno"]
        

        mobile_number_pattern = re.compile("^\+?\d{1,3}?[-.\s]?\d{9,12}$")

        if len(recruiter_user_mobileno) > 0:
            if not re.search(mobile_number_pattern, recruiter_user_mobileno):
                raise serializers.ValidationError({'errorMsg':'Invalid Mobile no.'})
        
        return data
    


