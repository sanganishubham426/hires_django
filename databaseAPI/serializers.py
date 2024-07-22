from rest_framework import serializers
from .models import *
import re
import string
import random
from datetime import datetime

class SectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = SectorModel
        fields = ["sector_name","sector_action","sector_name_arabic"]
    
    def validate(self, data):
        sector_name=data["sector_name"]
    
        if sector_name == None or sector_name == "":
            raise serializers.ValidationError({'errorMsg' : 'Sector name is required'})
        data["sector_name"] = data["sector_name"].lower()
        return data

class JobPositionSerializer(serializers.ModelSerializer):

    sector_id = serializers.PrimaryKeyRelatedField(queryset=SectorModel.objects.all(), source='sector')

    class Meta:
        model = JobPositionModel
        fields = ["job_position_name","sector_id","job_position_action","job_position_name_arabic"]

    def validate(self, data):
        job_position_name=data["job_position_name"]

        if job_position_name == None or job_position_name == "":
            raise serializers.ValidationError({'errorMsg' : 'Job Position name is required'})
        data["job_position_name"] = data["job_position_name"].lower()
        return data

class JobLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobLevelModel
        fields = ["job_level_name","job_level_action","job_level_name_arabic"]
    
    def validate(self, data):
        job_level_name=data["job_level_name"]
    
        if job_level_name == None or job_level_name == "":
            raise serializers.ValidationError({'errorMsg' : 'Job level name is required'})
        data["job_level_name"] = data["job_level_name"].lower()
        return data
