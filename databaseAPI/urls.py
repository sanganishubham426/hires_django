from django.contrib import admin
from django.urls import path
from . import views

from  django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('sectorRegister',views.SectorAPI.as_view() , name="sectorPage"),
    path('sectorUpdate',views.SectorUpdateAPI.as_view() , name="sectorUpdatePage"),
    path('sectorGet',views.SectorGetAPI.as_view() , name="sectorGetPage"),
    path('sectorGetOne',views.SectorGetOneAPI.as_view() , name="sectorGetOnePage"),
    path('sectorGetAction',views.SectorGetActionAPI.as_view() , name="sectorGetActionPage"),
    path('sectorDelete',views.SectorDeleteAPI.as_view() , name="sectorDeletePage"),
    path('SectorGetBySearch',views.SectorGetBySearchAPI.as_view() , name="SectorGetBySearchPage"),

    path('jobPositionRegister',views.JobPositionAPI.as_view() , name="jobPositionRegisterPage"),
    path('jobPositionUpdate',views.JobPositionUpdateAPI.as_view() , name="jobPositionUpdatePage"),
    path('jobPositionGet',views.JobPositionGetAPI.as_view() , name="jobPositionGetPage"),
    path('jobPositionGetOne',views.JobPositionGetOneAPI.as_view() , name="jobPositionGetOnePage"),
    path('jobPositionGetSector',views.JobPositionGetSectorAPI.as_view() , name="jobPositionGetSectorPage"),
    path('jobPositionDelete',views.JobPositionDeleteAPI.as_view() , name="jobPositionDeletePage"),
    path('JobPositionGetBySearch',views.JobPositionGetBySearchAPI.as_view() , name="JobPositionGetBySearchPage"),

    path('jobLevelRegister',views.JobLevelAPI.as_view() , name="jobLevelRegisterPage"),
    path('jobLevelUpdate',views.JobLevelUpdateAPI.as_view() , name="jobLevelUpdatePage"),
    path('jobLevelGet',views.JobLevelGetAPI.as_view() , name="jobLevelGetPage"),
    path('jobLevelGetOne',views.JobLevelGetOneAPI.as_view() , name="jobLevelGetOnePage"),
    path('jobLevelGetAction',views.JobLevelGetActionAPI.as_view() , name="jobLevelGetActionPage"),
    path('jobLevelDelete',views.JobLevelDeleteAPI.as_view() , name="jobLevelDeletePage"),
    path('JobLevelGetBySearch',views.JobLevelGetBySearchAPI.as_view() , name="JobLevelGetBySearchPage"),

    
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
