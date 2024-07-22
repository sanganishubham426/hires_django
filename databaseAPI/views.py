from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from .serializers import *
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse
import string
import random
import os
from userloginAPI.models import RecruiterModel
from databaseAPI.models import *
import json
from hires.emailsend import mailSend
from datetime import datetime, timedelta
from django.conf import settings
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
# from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

#######################################
#######################################

class SectorAPI(APIView):
    '''
        Sector API(INSERT)
        Request : POST
        Data =  {
                    "sector_name": "Health care",
                    "sector_action": "active"
                }
    '''
    def post(self, request ,format=None):

        getData = request.data
        
        if not SectorModel.objects.filter(sector_name=getData["sector_name"].lower()).exists():

            randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))
            uniqueID = "hires_sector_" + randomstr
            getData["sector_id"] = uniqueID
            serializer = SectorSerializer(data=getData)
            if serializer.is_valid():
                serializer.save(sector_id=getData["sector_id"])
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Sector is Added",
                    "Data": {
                        "sector_id" : getData['sector_id']
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
                    "Message": "Sector is already exits",
                    "Data": []
                    }
                return Response(res, status=status.HTTP_401_UNAUTHORIZED)

class SectorUpdateAPI(APIView):
    '''
        Sector API(Update)
        Request : Patch
        Data =  {
                    "sector_id": "hires_sector_m8kbwab2rehksfm",
                    "sector_name": "Information Technology",
                    "sector_action": "active"
                }
    '''
    def patch(self, request, format=None):
        getData = request.data # data comes from post request

        if not SectorModel.objects.filter(sector_name=getData["sector_name"].lower()).exists():

            if SectorModel.objects.filter(sector_id = getData["sector_id"]).exists():
                serializer = SectorSerializer(data=getData)

                if serializer.is_valid():
                    LastUpdateData = SectorModel.objects.get(sector_id = getData["sector_id"])
                    LastUpdateData.sector_name=getData["sector_name"].lower()
                    LastUpdateData.sector_action = getData["sector_action"]
                    LastUpdateData.save()
                    res = {
                        "Status": "success",
                        "Code": 200,
                        "Message": "Sector is Updated",
                        "Data": getData
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
                    "Message": "Sector data is not found",
                    "Data": []
                    }
                return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Sector is already exits",
                "Data": []
                }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)

class SectorGetAPI(APIView):
    '''
        Sector API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        sectorDetails = SectorModel.objects.values()
        res = {
                "Status": "success",
                "Code": 200,
                "Message": "Sector Details",
                "Data": sectorDetails
            }
        return Response(res, status=status.HTTP_200_OK)

class SectorGetOneAPI(APIView):
    '''
        Get One Sector API(View)
        Request : POST
        Data =  {
                    "sector_id": "hires_sector_ks5th0xuavqnehs"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if SectorModel.objects.filter(sector_id = getData["sector_id"]).exists():
            sectorDetail = SectorModel.objects.get(sector_id = getData["sector_id"])
            res = {
                    "Status": "success",
                    "Code": 200,
                    "Message": "Sector Detail",
                    "Data": {
                        "sector_id": getData["sector_id"],
                        "sector_name": sectorDetail.sector_name,
                        "sector_action": sectorDetail.sector_action
                    }
                }
            return Response(res, status=status.HTTP_200_OK)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Sector data is not found",
                "Data": []
                }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)

class SectorGetActionAPI(APIView):
    '''
        Get Action Sector API(View)
        Request : POST
        Data =  {
                    "sector_action": "active" #deactive
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        sectorDetails = SectorModel.objects.filter(sector_action = getData["sector_action"]).values()
        res = {
                "Status": "success",
                "Code": 200,
                "Message": "Sector Detail",
                "Data": sectorDetails
            }
        return Response(res, status=status.HTTP_200_OK)

class SectorDeleteAPI(APIView):
    '''
        Sector API(delete)
        Request : delete
        Data =  {
                    "sector_id":"hires_sector_ks5th0xuavqnehs"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if SectorModel.objects.filter(sector_id = getData["sector_id"]).exists():
            sectorDetail = SectorModel.objects.get(sector_id = getData["sector_id"])
            sectorDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 200,
                    "Message": "Sector is successfully Deleted",
                    "Data": []
                }
            return Response(res, status=status.HTTP_200_OK)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Sector data is not found",
                "Data": []
                }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)

class SectorGetBySearchAPI(APIView):

    def post(self, request, format=None):

        getData = request.data

        page = getData["page"]
        limit = getData["limit"]
        search_query = getData["q"]


        sectorDetails = SectorModel.objects.all()
        if search_query:
            sectorDetails = sectorDetails.filter(Q(sector_name__istartswith=search_query))

        paginator = Paginator(sectorDetails, limit)
        try:
            sectorDetails = paginator.page(page)
        except PageNotAnInteger:
            sectorDetails = paginator.page(1)
        except EmptyPage:
            sectorDetails = paginator.page(paginator.num_pages)

        serialized_data = [{'sector_id': sector.sector_id, 'sector_name': sector.sector_name,'sector_name_arabic':sector.sector_name_arabic,
                            'sector_action': sector.sector_action, 'sector_registration_date': sector.sector_registration_date}
                           for sector in sectorDetails]

        res = {
            "Status": "success",
            "Code": 200,
            "Message": "sector Details",
            "Data": {
                "serialized_data": serialized_data,
                "TotalPages": paginator.num_pages,
                "CurrentPage": page,
            }
        }

        return Response(res, status=status.HTTP_200_OK)

########################################################################
#Job Position#

class JobPositionAPI(APIView):

    '''
        job Position API(INSERT)
        Request : POST
        Data =  {
                    "sector_id": "hires_sector_ks5th0xuavqnehs",
                    "job_position_name": "Python Developer",
                    "job_position_action": "active"
                }
    '''
    def post(self, request ,format=None):

        getData = request.data
        if SectorModel.objects.filter(sector_id=getData["sector_id"]).exists():

            if not JobPositionModel.objects.filter(sector_id=getData["sector_id"],job_position_name=getData["job_position_name"].lower()).exists():
        
                randomstr = ''.join(random.choices(string.ascii_lowercase +
                                    string.digits, k=15))

                uniqueID = "hires_job_position_" + randomstr
                getData["job_position_id"] = uniqueID

                serializer = JobPositionSerializer(data=getData)

                if serializer.is_valid():
                    serializer.save(job_position_id=getData["job_position_id"])
                    res = {
                        "Status": "success",
                        "Code": 201,
                        "Message": "Job Position is Added",
                        "Data": {
                            "job_position_id" : getData['job_position_id']
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
                    "Message": "Job Position is already exits",
                    "Data": []
                    }
                return Response(res, status=status.HTTP_401_UNAUTHORIZED)

        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Sector is not found",
                "Data": []
                }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)

class JobPositionUpdateAPI(APIView):
    '''
        Job Position API(Update)
        Request : Patch
        Data =  {
                    "job_position_id": "hires_job_position_3cgqmz8fp6vhc26",
                    "job_position_name": "Data Scientist",
                    "sector_id": "hires_sector_m8kbwab2rehksfm",
                    "job_position_action": "active"
                }
    '''
    def patch(self, request, format=None):
        getData = request.data # data comes from post request
        if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
            if not JobPositionModel.objects.filter(sector_id=getData["sector_id"], job_position_name=getData["job_position_name"].lower()).exists():
                if SectorModel.objects.filter(sector_id=getData["sector_id"]).exists():
                    serializer = JobPositionSerializer(data=getData)
                    if serializer.is_valid():
                        LastUpdateData = JobPositionModel.objects.get(job_position_id = getData["job_position_id"])
                        LastUpdateData.job_position_name = getData["job_position_name"].lower()
                        LastUpdateData.sector_id = getData["sector_id"]
                        LastUpdateData.job_position_action = getData["job_position_action"]
                        LastUpdateData.save()
                        res = {
                            "Status": "success",
                            "Code": 200,
                            "Message": "Job Position is Updated",
                            "Data": getData
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
                        "Message": "Sector is not found",
                        "Data": []
                        }
                    return Response(res, status=status.HTTP_401_UNAUTHORIZED)
            else:
                res = {
                    "Status": "error",
                    "Code": 401,
                    "Message": "Sector data with Job Position field is already exists",
                    "Data": []
                    }
                return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Job Position data is not found",
                "Data": []
                }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)

class JobPositionGetAPI(APIView):
    '''
        JobPosition API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        jobPositionDetails = JobPositionModel.objects.values()
        res = {
                "Status": "success",
                "Code": 200,
                "Message": "Job Position Details",
                "Data": jobPositionDetails
                }
        return Response(res, status=status.HTTP_200_OK)

class JobPositionGetOneAPI(APIView):
    '''
        Get One Field API(View)
        Request : POST
        Data =  {
                    "job_position_id": "hires_job_position_3cgqmz8fp6vhc26"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
            jobPositionDetail = JobPositionModel.objects.get(job_position_id = getData["job_position_id"])
            res = {
                    "Status": "success",
                    "Code": 200,
                    "Message": "job Position Field Detail",
                    "Data": {
                        "job_position_id": getData["job_position_id"],
                        "job_position_name": jobPositionDetail.job_position_name,
                        "sector_id": jobPositionDetail.sector_id,
                        "sector_name": jobPositionDetail.sector.sector_name,
                        "job_position_action": jobPositionDetail.job_position_action
                    }
                }
            return Response(res, status=status.HTTP_200_OK)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "job Position Field data is not found",
                "Data": []
                }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)

class JobPositionGetSectorAPI(APIView):
    '''
        Get Field Sector API(View)
        Request : POST
        Data =  {
                    "sector_id": "hires_sector_ks5th0xuavqnehs"
                    "job_position_action": "active"                          # "deactive" / "all"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if JobPositionModel.objects.filter(sector_id = getData["sector_id"]).exists():
            if getData["job_position_action"] == "active":
                jobPositionDetail = JobPositionModel.objects.filter(sector_id = getData["sector_id"], job_position_action = "active").values()
            elif getData["job_position_action"] == "deactive":
                jobPositionDetail = JobPositionModel.objects.filter(sector_id = getData["sector_id"], job_position_action = "deactive").values()
            else:
                jobPositionDetail = JobPositionModel.objects.filter(sector_id = getData["sector_id"]).values()
            res = {
                    "Status": "success",
                    "Code": 200,
                    "Message": "Sectorwise Job Position Detail",
                    "Data": jobPositionDetail
                }
            return Response(res, status=status.HTTP_200_OK)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Job Position data is not found",
                "Data": []
                }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)

class JobPositionDeleteAPI(APIView):
    '''
        JobPosition API(delete)
        Request : delete
        Data =  {
                    "job_position_id": "hires_job_position_3cgqmz8fp6vhc26"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if JobPositionModel.objects.filter(job_position_id = getData["job_position_id"]).exists():
            jobPositionDetail = JobPositionModel.objects.get(job_position_id = getData["job_position_id"])
            jobPositionDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 200,
                    "Message": "Job Position is successfully Deleted",
                    "Data": []
                }
            return Response(res, status=status.HTTP_200_OK)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Job Position data is not found",
                "Data": []
                }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)

class JobPositionGetBySearchAPI(APIView):

    def post(self, request, format=None):

        getData = request.data

        page = getData["page"]
        limit = getData["limit"]
        search_query = getData["q"]


        jobPositionDetails = JobPositionModel.objects.all()
        if search_query:
            jobPositionDetails = jobPositionDetails.filter(Q(job_position_name__istartswith=search_query))

        paginator = Paginator(jobPositionDetails, limit)
        try:
            jobPositionDetails = paginator.page(page)
        except PageNotAnInteger:
            jobPositionDetails = paginator.page(1)
        except EmptyPage:
            jobPositionDetails = paginator.page(paginator.num_pages)

        serialized_data = [{'sector_id':jobPos.sector_id,'job_position_id': jobPos.job_position_id, 'job_position_name': jobPos.job_position_name,'job_position_name_arabic':jobPos.job_position_name_arabic,
                            'job_position_action': jobPos.job_position_action, 'job_position_registration_date': jobPos.job_position_registration_date}
                           for jobPos in jobPositionDetails]

        res = {
            "Status": "success",
            "Code": 200,
            "Message": "job Position Details",
            "Data": {
                "serialized_data":serialized_data,
                "TotalPages": paginator.num_pages,
                "CurrentPage": page
            }
        }

        return Response(res, status=status.HTTP_200_OK)

########################################################################
#Job Level#

class JobLevelAPI(APIView):
    '''
        Job level API(INSERT)
        Request : POST
        Data =  {
                    "job_level_name": "Intern",
                    "job_level_action": "active"
                }
    '''
    def post(self, request ,format=None):

        getData = request.data
        
        if not JobLevelModel.objects.filter(job_level_name=getData["job_level_name"].lower()).exists():

            randomstr = ''.join(random.choices(string.ascii_lowercase +
                                string.digits, k=15))
            uniqueID = "hires_job_level_" + randomstr
            getData["job_level_id"] = uniqueID
            serializer = JobLevelSerializer(data=getData)
            if serializer.is_valid():
                serializer.save(job_level_id=getData["job_level_id"])
                res = {
                    "Status": "success",
                    "Code": 201,
                    "Message": "Job Level is Added",
                    "Data": {   "job_level_id" : getData['job_level_id']
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
                    "Message": "Job level is already exits",
                    "Data": []
                    }
                return Response(res, status=status.HTTP_401_UNAUTHORIZED)

class JobLevelUpdateAPI(APIView):
    '''
        JobLevel API(Update)
        Request : Patch
        Data =  {
                    "job_level_id": "hires_job_level_xu67gtz3c87zspr",
                    "job_level_name": "Junior",
                    "job_level_action": "active"
                }
    '''
    def patch(self, request, format=None):
        getData = request.data # data comes from post request

        if not JobLevelModel.objects.filter(job_level_name=getData["job_level_name"].lower()).exists():

            if JobLevelModel.objects.filter(job_level_id = getData["job_level_id"]).exists():
                serializer = JobLevelSerializer(data=getData)

                if serializer.is_valid():
                    LastUpdateData = JobLevelModel.objects.get(job_level_id = getData["job_level_id"])
                    LastUpdateData.job_level_name=getData["job_level_name"].lower()
                    LastUpdateData.job_level_action = getData["job_level_action"]
                    LastUpdateData.save()
                    res = {
                        "Status": "success",
                        "Code": 200,
                        "Message": "Job Level is Updated",
                        "Data": getData
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
                    "Message": "Job Level data is not found",
                    "Data": []
                    }
                return Response(res, status=status.HTTP_401_UNAUTHORIZED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Job Level is already exits",
                "Data": []
                }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)

class JobLevelGetAPI(APIView):
    '''
        JobLevel API(View)
        Request : GET
    '''
    def get(self, request, format=None):
        getData = request.data
        jobLevelDetails = JobLevelModel.objects.values()
        res = {
                "Status": "success",
                "Code": 200,
                "Message": "Job Level Details",
                "Data": jobLevelDetails
            }
        return Response(res, status=status.HTTP_200_OK)

class JobLevelGetOneAPI(APIView):
    '''
        Get One JobLevel API(View)
        Request : POST
        Data =  {
                    "job_level_id": "hires_job_level_xu67gtz3c87zspr"
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        if JobLevelModel.objects.filter(job_level_id = getData["job_level_id"]).exists():
            jobLevelDetail = JobLevelModel.objects.get(job_level_id = getData["job_level_id"])
            res = {
                    "Status": "success",
                    "Code": 200,
                    "Message": "Job Level Detail",
                    "Data": {
                        "job_level_id": getData["job_level_id"],
                        "job_level_name": jobLevelDetail.job_level_name,
                        "job_level_action": jobLevelDetail.job_level_action
                    }
                }
            return Response(res, status=status.HTTP_200_OK)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Job Level data is not found",
                "Data": []
                }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)

class JobLevelGetActionAPI(APIView):
    '''
        Get Action JobLevel API(View)
        Request : POST
        Data =  {
                    "job_level_action": "active" #deactive
                }
    '''
    def post(self, request, format=None):
        getData = request.data
        jobLevelDetails = JobLevelModel.objects.filter(job_level_action = getData["job_level_action"]).values()
        res = {
                "Status": "success",
                "Code": 200,
                "Message": "job Level Detail",
                "Data": jobLevelDetails
            }
        return Response(res, status=status.HTTP_200_OK)

class JobLevelDeleteAPI(APIView):
    '''
        JobLevel API(delete)
        Request : delete
        Data =  {
                    "job_level_id": "hires_job_level_xu67gtz3c87zspr"
                }
    '''
    def delete(self, request, format=None):
        getData = request.data
        if JobLevelModel.objects.filter(job_level_id = getData["job_level_id"]).exists():
            jobLevelDetail = JobLevelModel.objects.get(job_level_id = getData["job_level_id"])
            jobLevelDetail.delete()
            res = {
                    "Status": "success",
                    "Code": 200,
                    "Message": "Job Level is successfully Deleted",
                    "Data": []
                }
            return Response(res, status=status.HTTP_201_CREATED)
        else:
            res = {
                "Status": "error",
                "Code": 401,
                "Message": "Job Level data is not found",
                "Data": []
                }
            return Response(res, status=status.HTTP_401_UNAUTHORIZED)

class JobLevelGetBySearchAPI(APIView):

    def post(self, request, format=None):

        getData = request.data

        page = getData["page"]
        limit = getData["limit"]
        search_query = getData["q"]


        jobLevelDetails = JobLevelModel.objects.all()
        if search_query:
            jobLevelDetails = jobLevelDetails.filter(Q(job_level_name__istartswith=search_query))

        paginator = Paginator(jobLevelDetails, limit)
        try:
            jobLevelDetails = paginator.page(page)
        except PageNotAnInteger:
            jobLevelDetails = paginator.page(1)
        except EmptyPage:
            jobLevelDetails = paginator.page(paginator.num_pages)

        serialized_data = [{'job_level_id': jobLevel.job_level_id, 'job_level_name': jobLevel.job_level_name,'job_level_name_arabic':jobLevel.job_level_name_arabic,
                            'job_level_action': jobLevel.job_level_action, 'job_level_registration_date': jobLevel.job_level_registration_date}
                           for jobLevel in jobLevelDetails]

        res = {
            "Status": "success",
            "Code": 200,
            "Message": "job Level Details",
            "Data": {
                "serialized_data":serialized_data,
                "TotalPages": paginator.num_pages,
                "CurrentPage": page,
            }
        }

        return Response(res, status=status.HTTP_200_OK)

########################################################################