from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render
from django.template.context_processors import request
from rest_framework import permissions, viewsets, serializers

from .custom_permissions import IsOwnerOrAdmin
from .serializers import ResumeSerializer
# from django_renderpdf.views import PDFView  # <--- New
from rest_framework import generics, permissions, viewsets

from .custom_permissions import IsOwnerOrAdmin
from .models import (EducationHistory, EmploymentHistory, Qualification,
                     Reference, Resume, Skill, WebLink)


# class ResumePDFView(PDFView, generics.RetrieveAPIView):
#     queryset = Resume.objects.all()
#     serializer_class = ResumeSerializer
#
#     def get_context_data(self, *args, **kwargs):
#         """Pass some extra context to the template."""
#         context = super().get_context_data(*args, **kwargs)
#
#         resume = Resume.objects.get(id=kwargs["pk"])
#
#         context["resume"] = Resume.objects.get(id=kwargs["pk"])
#         context["employment_history"] = EmploymentHistory.objects.filter(
#             resume=resume.id
#         )
#         context["education_history"] = EducationHistory.objects.filter(resume=resume.id)
#         context["web_links"] = WebLink.objects.filter(resume=resume.id)
#         context["skills"] = Skill.objects.filter(resume=resume.id)
#         context["qualifications"] = Qualification.objects.filter(resume=resume.id)
#         context["references"] = Reference.objects.filter(resume=resume.id)
#
#         # Gets the template_name dynamically
#         self.template_name = f"resumes/{context['resume'].resume_template.name}.html"
#         self.download_name = (
#             f"{context['resume'].resume_template.name}_{context['resume'].first_name}.pdf"
#         )
#         self.prompt_download = False
#
#         return context


def TestView(request):
    """user = User.objects.create_user("username=john", "email=lennon@thebeatles.com", "password=johnpassword")"""
    if request.method == "GET":
        user = User.objects.get(username="john")
        # user = User.objects.get(first_name="john")
        job_title = "Musician"
        first_name = "john"
        last_name = "lennon"
        email = "lennon@thebeatles.com"
        professional_summary = "Accomplished musician, songwriter, and cultural icon " \
                               "with extensive experience as a founding member of The Beatles," \
                               " renowned for shaping modern music and popular culture. Recognized" \
                               " for pioneering a unique songwriting style that combines rock," \
                               " introspection, and social commentary, contributing to over 200 " \
                               "globally celebrated songs. Proven solo artist with iconic works " \
                               "like Imagine, emphasizing peace and humanitarian values. Adept" \
                               " at creative collaboration and innovation, consistently producing" \
                               " impactful and influential music that resonates across generations."

        resume = Resume.objects.get(user_id=user, job_title=job_title, first_name=first_name, last_name=last_name,
                                    email=email, professional_summary=professional_summary)

        role = "Professor"
        employer = "CCSU"
        city = "New Britain"
        description = "N/A"
        start_date = "2020-12-23"
        end_date = None
        employment_history = EmploymentHistory.objects.create(resume=resume, role=role, employer=employer, city=city,
                                                              description=description,
                                                              start_date=start_date, end_date=end_date)

        degree = "B.S. in Computer Science"
        school = "CCSU"
        city = "New Britain"
        description = "N/A"
        start_date = "2020-12-23"
        end_date = None
        education_history = EducationHistory.objects.create(resume=resume, degree=degree, school=school, city=city,
                                                            description=description, start_date=start_date,
                                                            end_date=end_date)
        name = "LinkedIn"
        link = "linkedIn.com"
        weblink = WebLink.objects.create(resume=resume, name=name, link=link)

        skill = "communication"
        skills = Skill.objects.create(resume=resume, name=skill)

        resume.save()
        user.save()
        employment_history.save()
        education_history.save()
        weblink.save()
        skills.save()

        return HttpResponse("user and resume created")


def TestDisplayCasual(request):
    user = authenticate(username="john", password="johnpassword")
    resume = Resume.objects.get(user_id=user)
    employment_history = EmploymentHistory.objects.filter(resume=resume).order_by("-start_date")
    education_history = EducationHistory.objects.filter(resume=resume).order_by("-start_date")
    skills = Skill.objects.filter(resume=resume)
    web_links = WebLink.objects.filter(resume=resume)
    qualifications = Qualification.objects.filter(resume=resume)
    references = Reference.objects.filter(resume=resume)
    context = {
        "resume": resume,
        "employment_history": employment_history,
        "education_history": education_history,
        "skills": skills,
        "web_links": web_links,
        "qualifications": qualifications,
        "references": references,

    }

    return render(request, "casual.html", context)


def TestDisplayProfessional(request):
    user = authenticate(username="john", password="johnpassword")
    resume = Resume.objects.get(user_id=user)
    employment_history = EmploymentHistory.objects.filter(resume=resume).order_by("-start_date")
    education_history = EducationHistory.objects.filter(resume=resume).order_by("-start_date")
    skills = Skill.objects.filter(resume=resume)
    web_links = WebLink.objects.filter(resume=resume)
    qualifications = Qualification.objects.filter(resume=resume)
    references = Reference.objects.filter(resume=resume)
    context = {
        "resume": resume,
        "employment_history": employment_history,
        "education_history": education_history,
        "skills": skills,
        "web_links": web_links,
        "qualifications": qualifications,
        "references": references,

    }

    return render(request, "professional.html", context)


class ResumeViewset(viewsets.ModelViewSet):
    """
    list: List all resumes belonging to this authenticated user.
    create: Create a new resume as an authenticated user.
    retrieve: Retrieve resume (by ID) belonging to this authenticated user.
    partial_update: Update resume (by ID) belonging to this authenticated user.
    destroy: Delete resume (by ID) belonging to this authenticated user.
    """
    queryset = Resume.objects.all()  # the objects returned are actually determined by get_queryset
    """
    By setting serializer_class = ResumeSerializer, you tell the ResumeViewset to:

    Use ResumeSerializer for serializing Resume instances when sending data to the client.
    Use ResumeSerializer for deserializing incoming data when creating or updating Resume instances.
    """
    serializer_class = ResumeSerializer
    http_method_names = ["get", "post", "patch", "delete"]
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        """
        this line is only executed when a post request is NOT sent
        Purpose: (only authenticates if user is owner or admin)
        """
        if self.action != "create":
            return [IsOwnerOrAdmin()]
        return super().get_permissions()

    # overridden method from ModelViewSet
    def get_queryset(self):
        try:
            # if the user is a regular user return all of their own resumes
            if not self.request.user.is_staff or not self.request.user.is_superuser:
                return Resume.objects.filter(user_id=self.request.user)
        except Exception:
            return Resume.objects.none()
        # else (they are superuser) return resumes of everyone
        return super().get_queryset()

    def perform_create(self, serializer):

        # Pass the user and resume template to the serializer
        serializer.save(user=self.request.user)

# class DisplayResumeView(request):
#
#     permission_classes = [permissions.IsAuthenticated]
#
#     Resume.objects.filter(user_id=request.user)
