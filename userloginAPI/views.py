from django.shortcuts import render
from django.http import HttpResponse

from .models import *

from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from django.contrib.auth.hashers import make_password

import string
import random
import json

from hires.emailsend import *
from hires.google_info import *

from datetime import datetime, timedelta

from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed

from django.utils import timezone


# 

class UserRegisterAPI(APIView):

    '''
        User sign up api
        request = post
        data:
        {
            "recruiter_user_firstname": "yash",
            "recruiter_user_lastname": "patel",
            "recruiter_user_email":"patel4@gmail.com",
            "recruiter_user_password":"Patel2@",
        }
    '''
    def post(self, request, format=None):
        
        getData = request.data # data comes from post request  
        
        try:
            if not RecruiterModel.objects.filter(recruiter_user_email=getData["recruiter_user_email"].lower()).exists():
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=10))
                uniqueID = "hires_"+getData["recruiter_user_email"].split("@")[0]+"_"+randomstr
                getData["recruiter_user_id"] = uniqueID
                serializer = UserSerializer(data=getData)
                if serializer.is_valid():
                    # Generating code for email verification
                    randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=6))
                    
                    # Save the user to the database temporarily
                    user = serializer.save(recruiter_user_id=getData["recruiter_user_id"], recruiter_user_is_verified=False)

                    try:
                        # Try sending the email
                        emailStatus = mailSend(request, getData, randomstr)
                        
                        if emailStatus:
                            # Save email verification details if email is sent
                            userVerification = RecruiterEmailVerification(
                                                recruiter_user_id = getData["recruiter_user_id"],
                                                OTP_verify = randomstr,
                                                expire_time = datetime.now() + timedelta(minutes=10)
                                            )
                            userVerification.save()

                            # Response format
                            res = {
                                    "Status": "success",
                                    "Code": 200,
                                    "Message": "Account is created. Kindly check the mail and verify your account.",
                                    "Data": {
                                        "recruiter_user_id" : getData['recruiter_user_id']
                                    }
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                        else:
                            # If email sending failed, delete the user
                            user.delete()
                            res = {
                                "Status": "error",
                                "Code": 400,
                                "Message": "Something went wrong! Please check email",
                                "Data":[]
                            }
                            return Response(res, status=status.HTTP_400_BAD_REQUEST)
                    
                    except Exception as e:
                        # If email sending failed, delete the user
                        user.delete()
                        res = {
                            "Status": "error",
                            "Code": 400,
                            "Message": "Email send error",
                            "Data": []
                        }
                        return Response(res, status=status.HTTP_400_BAD_REQUEST)

                else:
                    res = {
                        "Status": "error",
                        "Code": 400,
                        "Message": list(serializer.errors.values())[0][0],
                        "Data": [],
                    }
                    return Response(res, status=status.HTTP_400_BAD_REQUEST)
            else:
                res = {
                    "Status": "error",
                    "Code": 400,
                    "Message": "Customer email already exists",
                    "Data": [],
                    }
                return Response(res, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            res = {
                "Status": "error",
                "Code": 400,
                "Message": str(e),
                "Data": [],
                }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)

class EmailVerificationAPI(APIView):

    '''
        Sending email verification code API
        request = post
        data = {
                "recruiter_user_id": "hires_patelyash2504_qiseymr4mo",
                }
    '''

    def post(self, request, format=None):
        
        getData = request.data # Get data from API request in json

        # if serializer.is_valid(): # Check validation

            # Generating code for email verification   
        randomstr = ''.join(random.choices(string.ascii_lowercase +
                            string.digits, k=6))


        # Check weather user exist or not in register table
        if RecruiterModel.objects.filter(recruiter_user_id = getData["recruiter_user_id"]).exists():
            
            # Check weather user exist or not in email veriication code table
            if RecruiterEmailVerification.objects.filter(recruiter_user_id = getData["recruiter_user_id"]).exists():


                userVerification = RecruiterEmailVerification.objects.get(recruiter_user_id = getData["recruiter_user_id"])
                
                # Check Code expiration time --- code only valid for 10 min
                FMT = "%H:%M:%S"
                current_time = datetime.now().strftime(FMT)
                store_time = userVerification.expire_time + timedelta(hours=5,minutes=30) 
                store_time = store_time.strftime(FMT)
                diff = datetime.strptime(store_time, FMT) > datetime.strptime(current_time, FMT)

                
                '''
                    if code is expired then new code with generate and updated in database
                '''
                if diff:
                    randomstr = userVerification.OTP_verify
                else:
                    userVerification.OTP_verify = randomstr
                    userVerification.expire_time = datetime.now() + timedelta(minutes=10)
                    userVerification.save()

            else:
                # if user data is not exist in verification table then insert it
                userVerification = RecruiterEmailVerification(
                                    recruiter_user_id = getData["recruiter_user_id"],
                                    OTP_verify = randomstr,
                                    expire_time = datetime.now() + timedelta(minutes=10)
                                        )
                userVerification.save()
                print(userVerification ,"KKKKKKKKKKKKKK")

            # Send a mail to user along with verification code
            if userVerification.recruiter_user:

                print("hhhhhh",userVerification)

                emailStatus = mailSend(request, getData, randomstr)
                print("KKKKKKKKKKKKKKKKKKKKKKKKK")
                if emailStatus:

                    # Response format
                    res = {
                            "Status": "success",
                            "Code": 200,
                            "Message":"Verification code is sent to your email. Kindly check it out",
                            "Data": {
                                "recruiter_user_id": getData["recruiter_user_id"]
                            }
                        
                        }
                    return Response(res, status=status.HTTP_200_OK)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message":"Email sending error",
                        "Data": []
                    }
                    return Response(res, status=status.HTTP_401_UNAUTHORIZED)

            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message":"User is not found",
                    "Data": []
                }
                return Response(res, status=status.HTTP_401_UNAUTHORIZED)

        else:

            res = {
                "Status": "error",
                "Code": 401,
                "Message":"User is not found",
                "Data": []
            }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
                
        # Error when data is invalid
        # res = {
        #         "Status": "error",
        #         "Code": 400,
        #         "Message": list(serializer.errors.values())[0][0],
        #         "Data": []
        #     }
        # return Response(res, status=status.HTTP_400_BAD_REQUEST)
               
class UserIdGetAPI(APIView):
    def post(self, request, format=None):
        recruiter_user_ids = RecruiterModel.objects.values_list('recruiter_user_id', flat=True)
        recruiter_user_id_list = list(recruiter_user_ids)

        res = { 
                    "Status": "success",
                    "Code": 200,
                    "Message":"Recruiter User Data",
                    "Data":{
                        "recruiter_user_id_list": recruiter_user_id_list
                    }
                }
        return Response(res, status=status.HTTP_200_OK)
    

class UserloggedInUpdateAPI(APIView):
    '''
        User sign up api
        request = patch
        data:
        {
            "recruiter_user_id": "hires_kishanpatel_thxj3yg643",
            "recruiter_user_is_loggedin: true
        }
    '''
    def patch(self, request, format=None):
        getData = request.data
        if RecruiterModel.objects.filter(recruiter_user_id = getData["recruiter_user_id"]).exists():
            userDetails = RecruiterModel.objects.get(recruiter_user_id = getData["recruiter_user_id"])
            userDetails.recruiter_user_is_loggedin = getData["recruiter_user_is_loggedin"]
            userDetails.save()
            res = { 
                    "Status": "success",
                    "Code": 200,
                    "Message":"Recruiter user loggedIn is updated",
                    "Data":{
                        "recruiter_user_id": getData["recruiter_user_id"],
                        "email": userDetails.recruiter_user_email,
                    }
                }
            return Response(res, status=status.HTTP_200_OK)
        else:
            res = { 
                    "Status": "error",
                    "Code": 401,
                    "Message":"Recruiter user is not found",
                    "Data": []
                }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        
class EmailVerificationCompletionAPI(APIView):

    '''
        Compare verification code and verified user account api
        request = patch (partial update) (used for only some columns needs to be updated)
        data = {
                "recruiter_user_id": "BroaderAI_patelyash2504_qiseymr4mo",
                "OTP_code":"738bqq"
            }
    '''
    def patch(self, request, format=None):

        getData = request.data

        # Check weather user exist or not in register table
        if RecruiterModel.objects.filter(recruiter_user_id = getData["recruiter_user_id"]).exists():

            # Check weather user exist or not in email veriication code table
            if RecruiterEmailVerification.objects.filter(recruiter_user_id = getData["recruiter_user_id"]).exists():

                userVerification = RecruiterEmailVerification.objects.get(recruiter_user_id = getData["recruiter_user_id"])

                # Check Code expiration time --- code only valid for 10 min
                FMT = "%H:%M:%S"
                current_time = datetime.now().strftime(FMT)
                store_time = userVerification.expire_time + timedelta(hours=5,minutes=30) 
                store_time = store_time.strftime(FMT)

                diff = datetime.strptime(store_time, FMT) > datetime.strptime(current_time, FMT)


                '''
                    if code is expired then new code with generate and updated in database
                '''

                if diff:

                    if userVerification.OTP_verify == getData["OTP_code"]:

                        myuser = RecruiterModel.objects.get(recruiter_user_id = getData["recruiter_user_id"])
                        myuser.recruiter_user_is_verified = True
                        myuser.save()

                        res = {
                                "Status": "success",
                                "Code": 200,
                                "Message": "Your account is verified", 
                                "Data":{
                                    "recruiter_user_id": getData["recruiter_user_id"]
                                }
                            }
                        return Response(res, status=status.HTTP_200_OK)

                    else:

                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message":"Verification Code doesn't match",
                            "Data": []
                            }
                        return Response(res, status=status.HTTP_401_UNAUTHORIZED)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message":"Verification code is expired",
                        "Data": []
                    }
                    return Response(res, status=status.HTTP_401_UNAUTHORIZED)

            else:

                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message":"User is not found",
                    "Data": []
                }
                return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message":"User is not found",
                    "Data": []
                }
                return Response(res, status=status.HTTP_401_UNAUTHORIZED)

class UserLoginAPI(APIView):

    '''
        User login API
        request = post
        data = {
                    "recruiter_user_email":"patelyash2504@gmail.com",
                    "recruiter_user_password":"Patelyash12@"
                }
    '''

    def post(self, request, format=None):

        getData = request.data

        print(getData)
        print("yyyy")
        serializer = LoginSerializer(data=getData)

        if serializer.is_valid(): # Check validation

            user = RecruiterModel.objects.get(recruiter_user_email=getData["recruiter_user_email"])
            
            # Response format
            res = {
                    "Status": "success",
                    "Code": 200,
                    "Message": "You are successfully login", 
                    "Data":{
                        "recruiter_user_id": user.recruiter_user_id,
                        "recruiter_user_email": getData["recruiter_user_email"],
                    }
                }
                
            return Response(res, status=status.HTTP_200_OK)

        print(serializer.errors)
        
        # Error when data is invalid
        res = {
                "Status": "error",
                "Code": 400,
                "Message": list(serializer.errors.values())[0][0],
                "Data": {
                    "recruiter_user_id": list(serializer.errors.values())[1][0]
                }
            }
        return Response(res, status=status.HTTP_400_BAD_REQUEST)


    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated]

class UserLogoutAPI(APIView):
    
    '''
        User logou API
        request = patch
        data = {
                    "recruiter_user_id":"hires_kishanpatel_thxj3yg643",
                }
    '''

    def patch(self, request, format=None):

        getData = request.data
        if RecruiterModel.objects.filter(recruiter_user_id = getData["recruiter_user_id"]).exists():
            
            user = RecruiterModel.objects.get(recruiter_user_id = getData["recruiter_user_id"])

            if user.recruiter_user_is_loggedin:
                
                user.recruiter_user_is_loggedin = False
                user.save()

                if user.recruiter_user_id:
                    res = {
                        "Status": "success",
                        "Code": 200,
                        "Message": "Succeessfully logout",
                        "Data":[]
                    }
                    return Response(res, status=status.HTTP_200_OK)

                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Something goes wrong while logout",
                        "Data": []
                    }
                    return Response(res, status=status.HTTP_401_UNAUTHORIZED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "You are not logged in",
                    "Data": []
                }
                return Response(res, status=status.HTTP_401_UNAUTHORIZED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message":"User is not found",
                "Data": []
            }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)

    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated]

class UserForgetPasswordAPI(APIView):
    '''
        Forget Password API
        request = post
        data = {
                    "recruiter_user_email":"patelyash2504@gmail.com"
                }
    '''

    def post(self, request, format=None):

        getData = request.data


        if RecruiterModel.objects.filter(recruiter_user_email=getData['recruiter_user_email']).exists():
            

            user = RecruiterModel.objects.get(recruiter_user_email=getData['recruiter_user_email'])

            if not user.recruiter_user_is_loggedin:

                randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=6))

                if RecruiterEmailVerification.objects.filter(recruiter_user_id = user.recruiter_user_id).exists():

                        userVerification = RecruiterEmailVerification.objects.get(recruiter_user_id = user.recruiter_user_id)
                        
                        # Check Code expiration time --- code only valid for 10 min
                        FMT = "%H:%M:%S"
                        current_time = datetime.now().strftime(FMT)
                        store_time = userVerification.expire_time + timedelta(hours=5,minutes=30) 
                        store_time = store_time.strftime(FMT)
                        diff = datetime.strptime(store_time, FMT) > datetime.strptime(current_time, FMT)

                        
                        '''
                            if code is expired then new code with generate and updated in database
                        '''
                        if diff:
                            randomstr = userVerification.OTP_verify
                        else:
                            userVerification.OTP_verify = randomstr
                            userVerification.expire_time = datetime.now() + timedelta(minutes=10)
                            userVerification.save()

                else:
                
                # if user data is not exist in verification table then insert it
                    userVerification = RecruiterEmailVerification(
                                        recruiter_user_id = user.recruiter_user_id,
                                        OTP_verify = randomstr,
                                        expire_time = datetime.now() + timedelta(minutes=10)
                                            )
                    userVerification.save() 


                # Send a mail to user along with verification code
                if userVerification.recruiter_user:

                    print("KKKKKKKKGGGGGGGGGG")
                    
                    myuser = dict()
                    myuser["recruiter_user_id"] = user.recruiter_user_id
                    emailStatus = mailSend(request, myuser, randomstr)
                    print("Grisha Sachani")
                    if emailStatus:

                        # Response format
                        res = {
                                "Status": "success",
                                "Code": 200,
                                "Message": "Verification code is sent to your email. Kindly check it out", 
                                "Data":{
                                    "recruiter_user_id": user.recruiter_user_email
                                }
                            }
                        return Response(res, status=status.HTTP_200_OK)

                    else:
                        res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Email sending error",
                                "Data":[]
                            }
                        return Response(res, status=status.HTTP_401_UNAUTHORIZED)

                else:
                    res = {
                            "Status": "error",
                            "Code": 401,
                            "Message":"User is not found",
                            "Data": []
                        }
                    return Response(res, status=status.HTTP_401_UNAUTHORIZED)

            else:
                res = {
                        "Status": "error",
                        "Code": 401,
                        "Message":"User is already loggedin",
                        "Data": []
                    }    
                return Response(res, status=status.HTTP_401_UNAUTHORIZED)      
        else:
            res = {
                    "Status": "error",
                    "Code": 401,
                    "Message":"Email does not existed",
                    "Data": []
                }    
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)

class ForgotPasswordChangedAPI(APIView):

    '''
        Create new password
        request = post
        data = {
                "recruiter_user_email":"patelyash2504@gmail.com",
                "recruiter_user_new_password":"Patelyash12@",
                "OTP_code": "Patelyash12@"
            } 
    '''

    def post(self, request, format=None):

        getData = request.data

        if RecruiterModel.objects.filter(recruiter_user_email=getData['recruiter_user_email']).exists():

            user = RecruiterModel.objects.get(recruiter_user_email=getData['recruiter_user_email'])

            if not user.recruiter_user_is_loggedin:
           
                # Check weather user exist or not in email veriication code table
                if RecruiterEmailVerification.objects.filter(recruiter_user_id = user.recruiter_user_id).exists():

                    userVerification = RecruiterEmailVerification.objects.get(recruiter_user_id = user.recruiter_user_id)

                    # Check Code expiration time --- code only valid for 10 min
                    FMT = "%H:%M:%S"
                    current_time = datetime.now().strftime(FMT)
                    store_time = userVerification.expire_time + timedelta(hours=5,minutes=30) 
                    store_time = store_time.strftime(FMT)

                    diff = datetime.strptime(store_time, FMT) > datetime.strptime(current_time, FMT)


                    '''
                        if code is expired then new code with generate and updated in database
                    '''

                    if diff:

                        if userVerification.OTP_verify == getData["OTP_code"]:

                            # Salt string for security
                            randomstr = ''.join(random.choices(string.ascii_letters +
                                                string.digits, k=10))

                            user.recruiter_user_password = make_password(getData["recruiter_user_new_password"],salt=randomstr, hasher='argon2')
                            user.save()

                            res = {
                                    "Status": "success",
                                    "Code": 200,
                                    "Message": "Your Password is changed. please login with new Password",
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_200_OK)

                        else:

                            res = {
                                    "Status": "error",
                                    "Code": 401,
                                    "Message": "Verification Code doesn't match",
                                    "Data":[],
                                }
                            return Response(res, status=status.HTTP_401_UNAUTHORIZED)

                    else:
                        res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Verification code is expired",
                                "Data":[],
                            }
                        return Response(res, status=status.HTTP_401_UNAUTHORIZED)

                else:

                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message":"User is not found",
                        "Data": []
                    }
                    return Response(res, status=status.HTTP_401_UNAUTHORIZED)
            
            else:
                res = {
                        "Status": "error",
                        "Code": 401,
                        "Message":"User is already loggedin",
                        "Data": []
                    }   
                return Response(res, status=status.HTTP_401_UNAUTHORIZED) 

        else:
            res = {
                    "Status": "error",
                    "Code": 401,
                    "Message":"Email does not existed",
                    "Data": []
                }   
            raise Response(res)

class UserChangePasswordAPI(APIView):
    '''
        Change Password
        request = patch
        data = {
                "recruiter_user_id": "BroaderAI_patelyash2504_qiseymr4mo",
                "recruiter_user_email":"patelyash2504@gmail.com",
                "recruiter_user_password":"Patelyash12@",
                "recruiter_user_new_password": "Patelyash12@"
            }
    '''

    def patch(self, request, format=None):
        getData = request.data

        if RecruiterModel.objects.filter(recruiter_user_id = getData["recruiter_user_id"]).exists():
            serializer = ChangePasswordSerializer(data=getData)

            if serializer.is_valid():
                
                user = RecruiterModel.objects.get(recruiter_user_id = getData["recruiter_user_id"])

                newpwd = getData["recruiter_user_new_password"]

                randomstr = ''.join(random.choices(string.ascii_letters +
                             string.digits, k=10))

                # Encrypt password with argon2 algorithms
                encrpt_pass = make_password(newpwd,salt=randomstr, hasher='argon2')
                user.recruiter_user_password = encrpt_pass
                user.save()

                res = {
                    "Status": "success",
                    "Code": 200,
                    "Message": "Your password is successfully changed.", 
                    "Data":{
                        "recruiter_user_id": getData["recruiter_user_id"],
                        "recruiter_user_email": getData["recruiter_user_email"]
                    }
                }
                return Response(res, status=status.HTTP_200_OK)

            # Error when data is invalid
            res = {
                "Status": "error",
                "Code": 400,
                "Message": list(serializer.errors.values())[0][0],
                "Data": []
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)


        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message":"User is not found",
                "Data": []
            }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)

    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated]


class UserEditProfileAPI(APIView):

    '''
        User edit profile api
        request = patch
        data:
        {
            "recruiter_user_id" : "BroaderAI_patelyash2504_ny5pq7a78s",
            "recruiter_user_mobileno" : "8462351478",

        }
    '''

    # request comes from post method
    def patch(self, request, format=None):
        
        getData = request.data

        if RecruiterModel.objects.filter(recruiter_user_id = getData["recruiter_user_id"]).exists():

            user = RecruiterModel.objects.get(recruiter_user_id = getData["recruiter_user_id"])

            user.recruiter_user_mobileno = getData["recruiter_user_mobileno"]
            
            user.save()

            res = {
                    "Status": "success",
                    "Code": 200,
                    "Message": "User Profile is updated.", 
                    "Data":{
                        "recruiter_user_id": getData["recruiter_user_id"]
                    }
                }

            return Response(res, status=status.HTTP_200_OK)

        else:

            res = {
                    "Status": "error",
                    "Code": 401,
                    "Message":"User is not found",
                    "Data": []
            }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)

    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated]


class ViewUserProfileAPI(APIView):

    '''
        User view profile api
        request = post
        data:
        {
            "recruiter_user_id" : "hires_kishanpatel_thxj3yg643",
        }
    '''

    # request comes from post method
    def post(self, request, format=None):
        
        getData = request.data

        if RecruiterModel.objects.filter(recruiter_user_id = getData["recruiter_user_id"]).exists():
            
            user = RecruiterModel.objects.get(recruiter_user_id = getData["recruiter_user_id"])

            if user.recruiter_user_is_loggedin:

                # if user.user_country is not None:

                #     nationalityData = NationalityModel.objects.get(nationality_id = user.user_country).nationality_name

                # else:

                #     nationalityData = ""


                userdetails = {
                    "recruiter_user_firstname": user.recruiter_user_firstname,
                    "recruiter_user_lastname": user.recruiter_user_lastname,
                    "recruiter_user_email": user.recruiter_user_email,
                    "recruiter_user_mobileno": user.recruiter_user_mobileno,
                }
                
                res = {
                        "Status": "success",
                        "Code": 200,
                        "Message": "User detail",
                        "Data":{
                            "userDetails": userdetails
                        }
                    }
                

            else:

                res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "You are not logged in",
                        "Data":[]
                    }
                return Response(res, status=status.HTTP_401_UNAUTHORIZED)

        else:

            res = {
                    "Status": "error",
                    "Code": 401,
                    "Message":"User is not found",
                    "Data": []
            }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)

        return Response(res, status=status.HTTP_200_OK)

    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated]
                        
# class GetUserdataAPI(APIView):
#     def post(self,format=None):                            
#         user = RecruiterModel.objects.order_by('-pk').last()
        
#         user_data = {
#         'recruiter_user_id': user.recruiter_user_id
#     }
#         res = {
#                 "Status": "success",
#                 "Code": 200,
#                 "Message": "User detail",
#                 "Data":{
#                     "userDetails": user_data
#                 }
#             }
#         return Response(res, status=status.HTTP_200_OK)

class GetUserdataAPI(APIView):
    '''
        JobLevel API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        recruiteruserDetails = RecruiterModel.objects.values()
        res = {
                "Status": "success",
                "Code": 200,
                "Message": "User Details",
                "Data": recruiteruserDetails
            }
        return Response(res, status=status.HTTP_200_OK)



    
    