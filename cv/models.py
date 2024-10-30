from django.db import models
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_delete


class Resume(models.Model):
    '''Resume model'''
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes')
    job_title = models.CharField(max_length=200)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    professional_summary = models.TextField()

    def __str__(self):
        return self.first_name


class EmploymentHistory(models.Model):
    '''Employment History model could include Internships and other work-related experiences'''
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='employment_history')
    role = models.CharField(max_length=200)
    employer = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Employment History'

    def __str__(self):
        return self.role


class EducationHistory(models.Model):
    '''Education history model'''
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='educational_history')
    degree = models.CharField(max_length=200)
    school = models.CharField(max_length=400)
    city = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)

    class Meta:
        # To give the model a proper plural form, else, Django names it "Education Historys"
        verbose_name_plural = 'Education History'

    def __str__(self):
        return self.degree


class WebLink(models.Model):
    '''Web link model includes Twitter and other social links.'''
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='links')
    name = models.CharField(max_length=50)
    link = models.CharField(max_length=1000, blank=False, null=False)

    def __str__(self):
        return self.name


class Skill(models.Model):
    '''Skills models which can be technical and non-technical'''
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='skills')
    name = models.CharField(max_length=100)
    is_soft_skill = models.BooleanField(default=False, blank=True)

    def __str__(self):
        return self.name


class Qualification(models.Model):
    '''Qualifications besides regular education'''
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='qualifications')
    course = models.CharField(max_length=200, blank=False, null=False)
    institution = models.CharField(max_length=200, blank=False, null=False)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=False, blank=False)

    def __str__(self):
        return self.course


class Reference(models.Model):
    '''Reference model holds the resume owner referees'''
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name='references')
    reference_full_name = models.CharField(max_length=500)
    company = models.CharField(max_length=1000)
    phone_number = models.CharField(max_length=17, blank=True, null=True)
    email = models.EmailField(null=False, blank=False)

    def __str__(self):
        return self.reference_full_name
