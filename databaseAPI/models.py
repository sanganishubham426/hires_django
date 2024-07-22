from django.db import models
import datetime
# Create your models here.

class SectorModel(models.Model):
    class Meta:
        db_table = "hires_sector_tb"
    sector_id = models.CharField(max_length= 60, primary_key=True, default=None)
    sector_name = models.CharField(max_length=100,blank=True, null=True, default=None)  # IT, Health, etc
    sector_name_arabic = models.CharField(max_length=100,blank=True, null=True, default=None)  # IT, Health, etc
    sector_action =  models.CharField(max_length=60,blank=True,null=True,default="active")
    sector_registration_date = models.DateTimeField(default=datetime.datetime.now())

class JobPositionModel(models.Model):
    class Meta:
        db_table = "hires_job_position_tb"
    sector = models.ForeignKey(SectorModel, on_delete=models.CASCADE, default=None)
    job_position_id = models.CharField(max_length=60, primary_key= True, default=None) # id of job position
    job_position_name = models.TextField(blank=True, null=True, default=None) #python developer, react, data scientist
    job_position_name_arabic = models.TextField(blank=True, null=True, default=None) #python developer, react, data scientist
    job_position_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    job_position_registration_date = models.DateTimeField(default=datetime.datetime.now())

class JobLevelModel(models.Model):
    class Meta:
        db_table = "hires_job_level_tb"

    job_level_id = models.CharField(max_length=60, primary_key= True, default=None) # id of job level
    job_level_name = models.TextField(blank=True, null=True, default=None) #intern, senior, junior
    job_level_name_arabic = models.TextField(blank=True, null=True, default=None) #intern, senior, junior
    job_level_action =  models.CharField(max_length=60,blank=True,null=True,default="active") # active/deactive
    job_level_registration_date = models.DateTimeField(default=datetime.datetime.now())