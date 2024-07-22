from django.contrib import admin
from django.urls import path, include
from . import views


from  django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('jobDescriptionRegister',views.JobDescriptionAPI.as_view() , name="jobDescriptionRegisterPage"),
    path('jobDescriptionUpdate',views.JobDescriptionUpdateAPI.as_view() , name="jobDescriptionUpdatePage"),
    path('jobDescriptionGet',views.JobDescriptionGetAPI.as_view() , name="jobDescriptionGetPage"),
    path('jobDescriptionGetOne',views.JobDescriptionGetOneAPI.as_view() , name="jobDescriptionGetOnePage"),
    path('jobDescriptionGetUser',views.JobDescriptionGetUserAPI.as_view() , name="jobDescriptionGetUserPage"),
    path('jobDescriptionGetfromJobPositionJobLevel',views.JobDescriptionGetfromJobPositionJobLevelAPI.as_view() , name="jobDescriptionGetfromJobPositionJobLevelPage"),
    path('jobDescriptionDelete',views.JobDescriptionDeleteAPI.as_view() , name="jobDescriptionDeletePage"),


    path('RecruiterBulkResumeAnalysis',views.RecruiterBulkResumeAnalysisAPI.as_view() , name="RecruiterBulkResumeAnalysisPage"), 
    path('RecruiterBulkResumeAnalysisAllData',views.RecruiterBulkResumeAnalysisViewAllAPI.as_view() , name="RecruiterBulkResumeAnalysisAllDataPage"),  
    path('recruiterCandidateResumeUpdate',views.RecruiterCandidateResumeUpdateAPI.as_view() , name="recruiterCandidateResumeUpdatePage"),  

  



] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
 
