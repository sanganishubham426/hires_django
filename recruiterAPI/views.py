from django.shortcuts import render
from .models import *
from django.core.exceptions import SuspiciousFileOperation
from django.http import HttpResponse
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
import string
import random
import os
from userloginAPI.models import *
from databaseAPI.models import *
from recruiterAPI.models import *
# from candidateresumeAPI.models import *
# from candidatePreferenceAPI.models import *
import json
from hires.emailsend import mailSend
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
import operator
# from userloginAPI.views import APIKeyAuthentication
import zipfile
import json


from .preference import aiComperision
from .extractResumeText import getResumeText

# import spacy

# nlp = spacy.load("en_core_web_sm")



###################################################################################################################################################

# Create your views here.

class JobDescriptionAPI(APIView):

    '''
        job Description API(INSERT)
        Request : POST
        Data =  {
                    "job_position_id": "hires_job_position_6d9xkfg8wr0nvml",
                    "job_level_id": "hires_job_level_gcs56oghq4ae0gf",
                    "recruiter_user_id":"hires_firsetest3_0yyhogjnlh",
                    "job_description_upload_file": grisha.pdf
                    "job_tilte": "Python Developer"
                    "job_description_action": "active"     # active/deactive/archive/draft
                }
    '''
    
    def post(self, request ,format=None):

        getData = request.data

        if RecruiterModel.objects.filter(recruiter_user_id=getData["recruiter_user_id"]).exists():

            user = RecruiterModel.objects.get(recruiter_user_id=getData["recruiter_user_id"])
            
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                JobPosition = JobPositionModel.objects.get(job_position_id=getData["job_position_id"])
                if  JobLevelModel.objects.filter(job_level_id=getData["job_level_id"]).exists():
                    JobLevel = JobLevelModel.objects.get(job_level_id=getData["job_level_id"])
                    if user.recruiter_user_is_loggedin:

                        if not request.FILES:
                                res = {
                                    "Status": "error",
                                    "Code": 400,
                                    "Message": "File is required",
                                    "Data": []
                                }
                                return Response(res, status=status.HTTP_400_BAD_REQUEST)
                        
                        randomstr = ''.join(random.choices(string.ascii_lowercase +
                                            string.digits, k=15))

                        uniqueID = "hires_job_description_" + randomstr
                        getData["job_description_id"] = uniqueID
                        
                        getData['job_position_name']=JobPosition.job_position_name
                        getData['job_level_name']=JobLevel.job_level_name
                        
                        serializer = JobDescriptionSerializer(data=getData)
                        if serializer.is_valid():
                            serializer.save(job_description_id=getData["job_description_id"])
                            res = {
                                "Status": "success",
                                "Code": 201,
                                "Message": "Job Description is Added",
                                "Data": {   
                                    "job_description_id" : getData['job_description_id']
                                }
                            }
                            return Response(res, status=status.HTTP_201_CREATED)
                        else:
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
                            "Message": "You are not logged in",
                            "Data": []
                            }
                        return Response(res, status=status.HTTP_401_UNAUTHORIZED)
                
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job level data is not found",
                        "Data": []
                        }
                    return Response(res, status=status.HTTP_401_UNAUTHORIZED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "job Position data is not found",
                    "Data": []
                    }
                return Response(res, status=status.HTTP_401_UNAUTHORIZED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data": []
                }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
    
    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated]
               
class JobDescriptionUpdateAPI(APIView):

    '''
        job Description API(UPDATE)
        Request : PATCH
        Data =  {
                    "job_description_id":"hires_job_description_6s8ceoxeahnp168",
                    "job_position_id": "hires_job_position_6d9xkfg8wr0nvml",
                    "job_level_id": "hires_job_level_gcs56oghq4ae0gf",
                    "recruiter_user_id":"hires_firsetest3_0yyhogjnlh",
                    "job_description_upload_file": grisha.pdf,
                    "job_tilte": "Python Developer",
                    "job_description_action": "active" # active/deactive/archive/draft
                }
    '''
    def patch(self, request ,format=None):
        getData = request.POST.copy()  # Make a mutable copy
        # print(getData["job_description_upload_file"])
        if "job_description_upload_file" in getData :
            if RecruiterModel.objects.filter(recruiter_user_id = getData["recruiter_user_id"]).exists():
                user = RecruiterModel.objects.get(recruiter_user_id=getData["recruiter_user_id"])
                if JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).exists():
                    if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                        JobPosition = JobPositionModel.objects.get(job_position_id=getData["job_position_id"])
                        if JobLevelModel.objects.filter(job_level_id = getData["job_level_id"]).exists():
                            JobLevel = JobLevelModel.objects.get(job_level_id=getData["job_level_id"])
                            if user.recruiter_user_is_loggedin:
                                serializer = JobDescriptionSerializer(data=getData)
                                getData['job_position_name']=JobPosition.job_position_name
                                getData['job_level_name']=JobLevel.job_level_name
                                if serializer.is_valid():
                                    LastUpdateData = JobDescriptionModel.objects.get(job_description_id = getData["job_description_id"])
                                    LastUpdateData.recruiter_user_id = getData['recruiter_user_id']
                                    LastUpdateData.job_position_id = getData["job_position_id"]
                                    LastUpdateData.job_level_id = getData["job_level_id"]
                                    LastUpdateData.job_description_upload_file = getData["job_description_upload_file"]
                                    LastUpdateData.job_tilte = getData["job_tilte"]
                                    LastUpdateData.job_description_action = getData["job_description_action"]
                                    LastUpdateData.job_position_name = JobPosition.job_position_name
                                    LastUpdateData.job_level_name = JobLevel.job_level_name
                                    LastUpdateData.save()
                                    res = {
                                        "Status": "success",
                                        "Code": 200,
                                        "Message": "Job Description is Updated",
                                        "Data": {
                                            "job_description_id": getData["job_description_id"],
                                        }
                                    }
                                    return Response(res, status=status.HTTP_200_OK)
                                else:
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
                                    "Message": "You are not logged in",
                                    "Data": []}
                                return Response(res, status=status.HTTP_401_UNAUTHORIZED)
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Job Level data is not found",
                                "Data": []}
                            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Job Position data is not found",
                            "Data": []}
                        return Response(res, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Description data is not found",
                        "Data": []}
                    return Response(res, status=status.HTTP_401_UNAUTHORIZED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User data is not found",
                        "Data": []}
                    return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        else:
            if RecruiterModel.objects.filter(recruiter_user_id = getData["recruiter_user_id"]).exists():
                user = RecruiterModel.objects.get(recruiter_user_id=getData["recruiter_user_id"])
                if JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"]).exists():
                    if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                        JobPosition = JobPositionModel.objects.get(job_position_id=getData["job_position_id"])
                        if JobLevelModel.objects.filter(job_level_id = getData["job_level_id"]).exists():
                            JobLevel = JobLevelModel.objects.get(job_level_id=getData["job_level_id"])
                            if user.recruiter_user_is_loggedin:
                                LastUpdateData = JobDescriptionModel.objects.get(job_description_id = getData["job_description_id"])
                                getData["job_description_upload_file"] = LastUpdateData.job_description_upload_file
                                serializer = JobDescriptionSerializer(data=getData)
                                getData['job_position_name']=JobPosition.job_position_name
                                getData['job_level_name']=JobLevel.job_level_name
                                if serializer.is_valid():
                                    LastUpdateData = JobDescriptionModel.objects.get(job_description_id = getData["job_description_id"])
                                    LastUpdateData.recruiter_user_id = getData['recruiter_user_id']
                                    LastUpdateData.job_position_id = getData["job_position_id"]
                                    LastUpdateData.job_level_id = getData["job_level_id"]
                                    LastUpdateData.job_tilte = getData["job_tilte"]
                                    LastUpdateData.job_description_action = getData["job_description_action"]
                                    LastUpdateData.job_position_name = JobPosition.job_position_name
                                    LastUpdateData.job_level_name = JobLevel.job_level_name
                                    LastUpdateData.save()
                                    res = {
                                        "Status": "success",
                                        "Code": 200,
                                        "Message": "Job Description is Updated",
                                        "Data": {
                                            "job_description_id": getData["job_description_id"],
                                        }
                                    }
                                    return Response(res, status=status.HTTP_200_OK)
                                else:
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
                                    "Message": "You are not logged in",
                                    "Data": []}
                                return Response(res, status=status.HTTP_401_UNAUTHORIZED)
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Job Level data is not found",
                                "Data": []}
                            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
                    else:
                        res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Job Position data is not found",
                            "Data": []}
                        return Response(res, status=status.HTTP_401_UNAUTHORIZED)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Description data is not found",
                        "Data": []}
                    return Response(res, status=status.HTTP_401_UNAUTHORIZED)
            else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User data is not found",
                        "Data": []}
                    return Response(res, status=status.HTTP_401_UNAUTHORIZED)
    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated]
         
class JobDescriptionDeleteAPI(APIView):
    '''
        job Description API(delete)
        Request : delete
        Data =  {
                    "job_description_id":"hires_job_description_6s8ceoxeahnp168",
                    "recruiter_user_id":"hires_firsetest3_0yyhogjnlh",
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if RecruiterModel.objects.filter(recruiter_user_id=getData["recruiter_user_id"]).exists():
            user = RecruiterModel.objects.get(recruiter_user_id=getData["recruiter_user_id"])
            if user.recruiter_user_is_loggedin:
                
                if JobDescriptionModel.objects.filter(job_description_id = getData["job_description_id"],recruiter_user_id=getData["recruiter_user_id"]).exists():
                    
                    JobDescriptionDetail = JobDescriptionModel.objects.get(job_description_id = getData["job_description_id"],recruiter_user_id=getData["recruiter_user_id"])
                    JobDescriptionDetail.delete()
                    res = {
                            "Status": "success",
                            "Code": 200,
                            "Message": "Job Description is successfully Deleted",
                            "Data": []
                        }
                    return Response(res, status=status.HTTP_200_OK)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Description data is not found",
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
                "Message": "User is not found",
                "Data": []
                }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)

    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated]
          
class JobDescriptionGetAPI(APIView):
    '''
        Job Description API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        JobDescriptionDetails = JobDescriptionModel.objects.values()
        res = {
                "Status": "success",
                "Code": 200,
                "Message": "Job Description Details",
                "Data": JobDescriptionDetails,
            }
        return Response(res, status=status.HTTP_200_OK)      

    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated]  
    
class JobDescriptionGetOneAPI(APIView):
    '''
        Get One Job Description API(View)
        Request : POST
        Data =  {
                    "recruiter_user_id":"hires_firsetest3_0yyhogjnlh",
                    "job_description_id":"hires_job_description_6s8ceoxeahnp168",
                    "job_description_action": "active",  # active/deactive/archive/draft
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if RecruiterModel.objects.filter(recruiter_user_id=getData["recruiter_user_id"]).exists():
            user = RecruiterModel.objects.get(recruiter_user_id=getData["recruiter_user_id"])
            
            if user.recruiter_user_is_loggedin:
                
                if JobDescriptionModel.objects.filter( recruiter_user_id=getData["recruiter_user_id"], job_description_id = getData["job_description_id"],job_description_action = getData["job_description_action"]).exists():
                    
                    JobDescriptionDetail = JobDescriptionModel.objects.filter(recruiter_user_id=getData["recruiter_user_id"] , job_description_id = getData["job_description_id"],job_description_action = getData["job_description_action"]).values()
                    res = {
                            "Status": "success",
                            "Code": 200,
                            "Message": "Job Description Detail",
                            "Data": JobDescriptionDetail

                        }
                    return Response(res, status=status.HTTP_200_OK)
                else:
                    res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "Job Description data is not found",
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
                "Message": "User is not found",
                "Data": []
                }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated]
    
class JobDescriptionGetUserAPI(APIView):
    '''
        Get One Job Description User API(View)
        Request : POST
        Data =  {
                    "recruiter_user_id": "hires_firsetest3_0yyhogjnlh",
                    "job_description_action": "active", # active/deactive/archive/draft
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        
        if RecruiterModel.objects.filter(recruiter_user_id=getData["recruiter_user_id"]).exists():
            user = RecruiterModel.objects.get(recruiter_user_id=getData["recruiter_user_id"])
            
            if user.recruiter_user_is_loggedin:
                
                if JobDescriptionModel.objects.filter(recruiter_user_id = getData["recruiter_user_id"],job_description_action = getData["job_description_action"]).exists():

                    JobDescriptionDetail = JobDescriptionModel.objects.filter(recruiter_user_id = getData["recruiter_user_id"],job_description_action = getData["job_description_action"]).values().order_by('-job_description_registration_date')


                    res = {
                            "Status": "success",
                            "Code": 200,
                            "Message": "Job Description Detail",
                            "Data": {
                                "JobDescriptionDetail":JobDescriptionDetail,
                                "Total_job_posts": len(JobDescriptionDetail)
                            }

                        }
                    return Response(res, status=status.HTTP_200_OK)
                else:
                    res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Job Description data is not found",
                            "Data": {
                                "Total_job_posts": 0
                            }
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
                "Message": "User is not found",
                "Data": []
                }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)
    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated]
    
class JobDescriptionGetfromJobPositionJobLevelAPI(APIView):
    '''
        Get One Job Description Job Level Job Position API(View)
        Request : POST
        Data =  {
                    "recruiter_user_id":"hires_firsetest3_0yyhogjnlh",
                    "job_level_id": "hires_job_level_gcs56oghq4ae0gf",
                    "job_position_id": "hires_job_position_6d9xkfg8wr0nvml",
                    "job_description_action": "active", # active/deactive/archive/draft
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if RecruiterModel.objects.filter(recruiter_user_id=getData["recruiter_user_id"]).exists():
            user = RecruiterModel.objects.get(recruiter_user_id=getData["recruiter_user_id"])
            if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
                if  JobLevelModel.objects.filter(job_level_id=getData["job_level_id"]).exists():
                    if user.recruiter_user_is_loggedin:
                        if JobDescriptionModel.objects.filter(recruiter_user_id=getData["recruiter_user_id"],job_level_id = getData["job_level_id"],job_position_id = getData["job_position_id"],job_description_action = getData["job_description_action"]).exists():
                            
                            JobDescriptionDetail = JobDescriptionModel.objects.filter(recruiter_user_id=getData["recruiter_user_id"],job_level_id = getData["job_level_id"],job_position_id = getData["job_position_id"],job_description_action = getData["job_description_action"]).values()
                            
                            res = {
                                    "Status": "success",
                                    "Code": 200,
                                    "Message": "Job Description Detail",
                                    "Data": JobDescriptionDetail
                                }
                            return Response(res, status=status.HTTP_201_CREATED)
                        
                        else:
                            res = {
                                "Status": "error",
                                "Code": 401,
                                "Message": "Job Description data is not found",
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
                        "Message": "Job level data is not found",
                        "Data": []
                        }
                    return Response(res, status=status.HTTP_401_UNAUTHORIZED)
                
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "job Position data is not found",
                    "Data": []
                    }
                return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "User is not found",
                "Data": []
                }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)        

    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated]
     

#####################################################

# Recruiter Bulk Resume Analysis

class RecruiterBulkResumeAnalysisAPI(APIView):


    '''
    Request : Post
    Json Data : {

        "recruiter_user_id" : hires_yashpatel1234_yj6mc5kcki,
        "recruiter_bulk_resume_upload" : resumes.zip
        "job_description_id" : hires_job_description_79qui4q0hbp18iq
    }
    
    '''


    def post(self, request, format=None):

        try:

            getData = request.data

            if RecruiterModel.objects.filter(recruiter_user_id = getData["recruiter_user_id"]).exists():

                user = RecruiterModel.objects.get(recruiter_user_id=getData["recruiter_user_id"])

                if  JobDescriptionModel.objects.filter(recruiter_user_id = getData["recruiter_user_id"], job_description_id=getData["job_description_id"]).exists():

                    if user.recruiter_user_is_loggedin:

                        if not request.FILES:
                             
                            return Response({"Error": "Zip file is required"}, status=status.HTTP_400_BAD_REQUEST)


                        randomstr = ''.join(random.choices(string.ascii_lowercase +
                                            string.digits, k=15))

                        uniqueID = "hires_recruiter_bulk_resume_" + randomstr
                        getData["recruiter_bulk_resume_upload_id"] = uniqueID
                        
                        serializer = RecruiterBulkResumeUploadSerializer(data=getData)


                        if serializer.is_valid():
                            
                            resp = serializer.data 

                            #store zip folder path in model
                            userRes = RecruiterBulkResumeUploadModel(
                                recruiter_bulk_resume_upload_id =  resp["recruiter_bulk_resume_upload_id"],
                                recruiter_user_id  = resp["recruiter_user_id"],
                                recruiter_bulk_resume_upload = getData["recruiter_bulk_resume_upload"],
                                )


                            userRes.save() #save model

                            #     #to unzip the zip folder
                            if userRes.pk:
                                print("grishasachani")
                                try:
                                    print("kkkkkkkkkkkkkkkkkkkkkkk")
                                    file_path = ""

                                    #get zip folder from model
                                    data = RecruiterBulkResumeUploadModel.objects.get(recruiter_bulk_resume_upload_id=resp["recruiter_bulk_resume_upload_id"], recruiter_user_id=resp["recruiter_user_id"])
                                    print("111111111111")
                                    original_path = str(data.recruiter_bulk_resume_upload) #zip folder path
                                    print("2222222")
                                    fullpath = settings.MEDIA_ROOT + "\\" + original_path.replace("/", "\\") #full zip folder path from e:


                                    fullpath = "media/" + original_path #full zip folder path from e:
                                    # fullpath = "/home/hires/media/" + original_path #full zip folder path from e:
                                    print("333333")

                                    target_directory = os.path.join(settings.MEDIA_ROOT, 'extracted_resumes') #make directory in media folder
                                    print("4444444")
                                    os.makedirs(target_directory, exist_ok=True)


                                    with zipfile.ZipFile(fullpath, 'r') as zip_ref: #unzip folder
                                        print("5555555")
                                        for file_name in zip_ref.namelist():
                                            print("66666666666")
                                            file_info = zip_ref.getinfo(file_name) #getting file name
                                            print("7777777777")
                                            if file_info.is_dir():
                                                print("*888888888")
                                                continue

                                            print("999999999999")


                                            file_path = os.path.join(target_directory, file_name) #full path for all unzip files
                                            print("10 10 10 10")

                                            if file_path.lower().endswith('.pdf'): #validation only lower and .pdf is allowed
                                                print("11 11 11 11 11 11 11")

                                                zip_ref.extract(file_name, target_directory)
                                                print("12 121 12 12 12 12 12")


                                                #store extracted file in new model
                                                randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
                                                uniqueID = "hires_recruiter_resume_candidate_" + randomstr
                                                print(uniqueID ,"13 13 13 13")

#########################################################################################  Ayaa thi agal print nai taytu except ma jatu re che
                                                try:

                                                    resumeText = getResumeText(file_path) #resume parsing for extracting text
                                                    print(resumeText ,"14 14141")
                                                except Exception as e:
                                                    
                                                    print("error", e)

                                                    resumeText = ''


                                                
                                                recZipfile = RecruiterResumeCandidateModel(
                                                    recruiter_resume_candidate_id=uniqueID,
                                                    recruiter_bulk_resume_upload_id=data.recruiter_bulk_resume_upload_id,
                                                    recruiter_user_id=data.recruiter_user_id,
                                                    # recruiter_resume_candidate_file_path=file_path.split("\media")[1].replace("\\","/"), 
                                                    recruiter_resume_candidate_file_path=file_path.split("/media")[1], 
                                                    recruiter_resume_candidate_extracted_text=resumeText
                                                    
                                                )
                                                print(recZipfile , "14 14 14 14")
                                                recZipfile.save()
                                                print(recZipfile , "15 15 15 15")
                                                



                                    if  JobDescriptionModel.objects.filter(recruiter_user_id = getData["recruiter_user_id"], job_description_id=getData["job_description_id"]).exists():
                                        print("ggggggggggg")
                                        uploadedjd = JobDescriptionModel.objects.get(recruiter_user_id = getData["recruiter_user_id"], job_description_id=getData["job_description_id"])

                                        jdpath = settings.MEDIA_ROOT + "/" + str(uploadedjd.job_description_upload_file)

                                        jdtext = getResumeText(jdpath)

                                        resumeText = RecruiterResumeCandidateModel.objects.filter(recruiter_user_id = getData["recruiter_user_id"],recruiter_bulk_resume_upload_id = data.recruiter_bulk_resume_upload_id).values()


                                        extracted_text = {}
                                        resume_list = []
                                        for resume in resumeText:

                                            person = ""

                                            extracted_text= {
                                                "recruiter_resume_candidate_file_path" : settings.BASE_URL + '/media' + resume['recruiter_resume_candidate_file_path'],
                                                # "text": resume['recruiter_resume_candidate_extracted_text'],
                                                "candidate_name": person,
                                                "aiCompPercentageScore" : float(aiComperision(jdtext,resume['recruiter_resume_candidate_extracted_text']))
                                                
                                                }


                                            randomstr = ''.join(random.choices(string.ascii_lowercase + string.digits, k=15))
                                            datauniqueID = "hires_recruiter_data_file_" + randomstr

                                            bulk_resume_instance = RecruiterResumeCandidateModel(
                                                recruiter_resume_candidate_id=datauniqueID,
                                                recruiter_user_id=getData["recruiter_user_id"], 
                                                job_description_id=getData["job_description_id"], 
                                                recruiter_resume_candidate_file_path=resume['recruiter_resume_candidate_file_path'],
                                                recruiter_resume_candidate_name=person,
                                                recruiter_resume_candidate_gender = getData['recruiter_resume_candidate_gender'],
                                                recruiter_resume_candidate_experience = getData['recruiter_resume_candidate_experience'],
                                                recruiter_resume_candidate_nationality = getData['recruiter_resume_candidate_nationality'],
                                                # recruiter_resume_candidate_gender = person,
                                                # recruiter_resume_candidate_experience = person,
                                                # recruiter_resume_candidate_nationality = person,
                                                recruiter_resume_candidate_ai_compare_score=float(aiComperision(jdtext,resume['recruiter_resume_candidate_extracted_text'])),
                                            )


                                            bulk_resume_instance.save()

                                            resume_list.append(extracted_text)

                                        sorted_resumes = sorted(resume_list, key=operator.itemgetter('aiCompPercentageScore'), reverse=True)


                                        res = {
                                                "Status": "success",
                                                "Code": 201,
                                                "Message": "Comparision Details",
                                                "Data":{
                                                        "recruiter_user_id":getData["recruiter_user_id"],
                                                        "job_description_id": getData["job_description_id"],
                                                        "aiCompPercentageScore":sorted_resumes
                                                }
                                            }


                                        return Response(res, status=status.HTTP_201_CREATED)

                                    else:
                                        print("ssssssssssssss")
                                        res = {
                                            "Status": "error",
                                            "Code": 401,
                                            "Message": "Job description file is not found",
                                            "Data": []
                                            }
                
                                        return Response(res, status=status.HTTP_401_UNAUTHORIZED)
                                        

                                    




                                except Exception as e:
                                    print("??????????????")
                                    print("Error : ", e)

                                    pass

                            

                        else:
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
                            "Message": "User is not loggedin",
                            "Data": []
                            }
                
                        return Response(res, status=status.HTTP_401_UNAUTHORIZED)



                else:
                    
                    res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Job description is not found",
                            "Data": []
                    }

                    return Response(res, status=status.HTTP_401_UNAUTHORIZED)

            else:

                res = {
                        "Status": "error",
                        "Code": 401,
                        "Message": "User is not found",
                        "Data": []
                }
                
                return Response(res, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:

            print(f"Error: {e}")



# Recruiter Bulk resume View by job description and User

class RecruiterBulkResumeAnalysisViewAllAPI(APIView):
    '''
    Get Recruiter Bulk Resume Analysis View All Data API(View)
    Request : POST
    Data =  {
                "recruiter_user_id":"hires_firsetest3_0yyhogjnlh",
                "job_description_id":"hires_job_description_6s8ceoxeahnp168",
            }
    '''
    def post(self, request, format=None):

        getData = request.data
        
        if RecruiterModel.objects.filter(recruiter_user_id=getData["recruiter_user_id"]).exists():
            user = RecruiterModel.objects.get(recruiter_user_id=getData["recruiter_user_id"])
            
            if user.recruiter_user_is_loggedin:
                
                if JobDescriptionModel.objects.filter( recruiter_user_id=getData["recruiter_user_id"], job_description_id = getData["job_description_id"]).exists():
                    
                    candidateData = RecruiterResumeCandidateModel.objects.filter(recruiter_user_id=getData["recruiter_user_id"] , job_description_id = getData["job_description_id"]).values()

                    # Sort data in descending order based on recruiter_resume_candidate_ai_compare_score
                    candidateData = sorted(candidateData, key=lambda x: (float(x['recruiter_resume_candidate_ai_compare_score']), x['recruiter_resume_candidate_file_path']), reverse=True)

                    # Format recruiter_resume_candidate_file_path with base URL
                    for resume in candidateData:
                        resume['recruiter_resume_candidate_file_path'] = settings.BASE_URL + '/media' + resume['recruiter_resume_candidate_file_path']

                    res = {
                            "Status": "success",
                            "Code": 201,
                            "Message": "candidate data",
                            "Data": candidateData

                    }

                    return Response(res, status=status.HTTP_201_CREATED)
                else:
                    res = {
                            "Status": "error",
                            "Code": 401,
                            "Message": "Job Description data is not found",
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
                    "Message": "User is not found",
                    "Data": []
                    }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)


class RecruiterCandidateResumeUpdateAPI(APIView):

    '''
        Recruiter Bulk Resume Analysis API(UPDATE)
        Request : PATCH
        Data : {

            "recruiter_user_id" : hires_yashpatel1234_yj6mc5kcki,
            "recruiter_resume_candidate_id" : hires_job_description_79qui4q0hbp18iq,
            "recruiter_resume_candidate_bookmark" : true

        }
    
    '''
    def patch(self, request ,format=None):
        getData = request.data

        if RecruiterModel.objects.filter(recruiter_user_id = getData["recruiter_user_id"]).exists():
            user = RecruiterModel.objects.get(recruiter_user_id=getData["recruiter_user_id"])
            
            if RecruiterResumeCandidateModel.objects.filter(recruiter_resume_candidate_id = getData["recruiter_resume_candidate_id"]).exists():
            
                if user.recruiter_user_is_loggedin:

                    CandidateResumeUpdateData = RecruiterResumeCandidateModel.objects.get(recruiter_resume_candidate_id = getData["recruiter_resume_candidate_id"])
                    CandidateResumeUpdateData.recruiter_user_id = getData['recruiter_user_id']
                    CandidateResumeUpdateData.recruiter_resume_candidate_bookmark = getData["recruiter_resume_candidate_bookmark"]
                    CandidateResumeUpdateData.save()
                    
                    res = {
                        "Status": "success",
                        "Code": 200,
                        "Message": "Candidate Resume Is Updated.Your Bookmark Is Save",
                        "Data": {
                            "recruiter_resume_candidate_id": getData["recruiter_resume_candidate_id"],
                        }
                    }
                    return Response(res, status=status.HTTP_200_OK)

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
                    "Message": "Recruiter Candidate Resume is not found",
                    "Data": []}
                return Response(res, status=status.HTTP_401_UNAUTHORIZED)
            
        else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "User data is not found",
                    "Data": []}
                return Response(res, status=status.HTTP_401_UNAUTHORIZED)

    # authentication_classes=[JWTAuthentication]
    # permission_classes=[IsAuthenticated]
  
