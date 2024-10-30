from django.contrib import admin
from cv import models   # new

# Register your models here.

# METHOD 1 in registering models
# admin.site.register(models.ResumeTemplate)
# admin.site.register(models.Resume)

# METHOD 2 in registering models.
# Note the extra brackets "()"
admin.site.register((
    models.Resume,
    models.EducationHistory,
    models.EmploymentHistory,
    models.Qualification,
    models.Reference,
    models.Skill,
    models.WebLink
))