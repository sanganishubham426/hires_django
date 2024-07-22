from django.db import models
import datetime
from userloginAPI.models import RecruiterModel
from databaseAPI.models import *

# Create your models here.

class JobDescriptionModel(models.Model):
    
    class Meta:
        db_table = "recruiter_job_desc_tb"

    recruiter_user = models.ForeignKey(RecruiterModel,on_delete=models.CASCADE,default=None)
    job_position = models.ForeignKey(JobPositionModel,on_delete=models.CASCADE,default=None)
    job_level = models.ForeignKey(JobLevelModel,on_delete=models.CASCADE,default=None)
    job_position_name = models.CharField(max_length=100,blank=False,null=False,default=None)
    job_level_name = models.CharField(max_length=100,blank=False,null=False,default=None)
    job_tilte = models.CharField(max_length=100,blank=True, null=True,default=None)
    job_description_id = models.CharField(max_length=100, primary_key= True, default=None) # id of job description
    job_description_upload_file = models.FileField(upload_to='job_descriptions/',blank=True,null=True,default=None)
    job_description_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    job_description_registration_date = models.DateTimeField(default=datetime.datetime.now())


#############################################################

class RecruiterBulkResumeUploadModel(models.Model):
    
    class Meta:
        db_table = "recruiter_bulk_resume_upload_tb"

    recruiter_bulk_resume_upload_id = models.CharField(max_length= 60, primary_key=True) 
    recruiter_user = models.ForeignKey(RecruiterModel, on_delete=models.CASCADE) #recruiter_user_id
    recruiter_bulk_resume_upload = models.FileField(upload_to='recruiter_resumesUpload/',default=None, blank=True)
    recruiter_bulk_resume_upload_registration_date = models.DateTimeField(default=datetime.datetime.now())


class RecruiterResumeCandidateModel(models.Model):

    class Meta:
        db_table = "recruiter_resume_candidate_tb"

    recruiter_resume_candidate_id = models.CharField(max_length= 60, primary_key=True)
    recruiter_user = models.ForeignKey(RecruiterModel, on_delete=models.CASCADE)
    job_description = models.ForeignKey(JobDescriptionModel,on_delete=models.CASCADE,default=None)
    recruiter_bulk_resume_upload = models.ForeignKey(RecruiterBulkResumeUploadModel,on_delete=models.CASCADE,default=None)
    recruiter_resume_candidate_file_path = models.TextField(blank=True, null=True, default=None)
    recruiter_resume_candidate_extracted_text = models.TextField(blank=True, null=True, default=None)
    recruiter_resume_candidate_name = models.CharField(max_length=50, blank=True, null=True, default=None)
    recruiter_resume_candidate_gender = models.CharField(max_length=10, blank=True, null=True, default=None)
    recruiter_resume_candidate_experience = models.CharField(max_length=50, blank=True, null=True, default=None)
    recruiter_resume_candidate_nationality = models.CharField(max_length=30, blank=True, null=True, default=None)
    recruiter_resume_candidate_url = models.TextField(blank=True, null=True, default=None)
    recruiter_resume_candidate_bookmark = models.BooleanField(default=False)
    recruiter_resume_candidate_firstpage_image = models.FileField(upload_to='resume_firstpage_images/',default=None, blank=True)
    recruiter_resume_candidate_ai_compare_score = models.CharField(max_length=10, blank=True, null=True, default=None)
    recruiter_resume_candidate_registration_date = models.DateTimeField(default=datetime.datetime.now())
