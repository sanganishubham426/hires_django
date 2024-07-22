from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(JobDescriptionModel)
admin.site.register(RecruiterBulkResumeUploadModel)
admin.site.register(RecruiterResumeCandidateModel)
