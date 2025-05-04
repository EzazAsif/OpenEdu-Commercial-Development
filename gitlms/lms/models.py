from django.db import models
import os
from django.conf import settings
from .contentUploadStratagy import *
from .contentUploadAdapter import ContentUploadAdapter
from django.contrib.auth.models import User  # Import the User model
from accounts.imageResizer import ImageResizeMixin

class Institute(ImageResizeMixin,models.Model):
    id = models.AutoField(primary_key=True)  # Automatically generates a primary key
    name = models.CharField(max_length=255, unique=True)  # Unique name field
    image = models.ImageField(upload_to='images/Institute/', null=True,default='images/Institute/default.jpg')  
    description = models.TextField( max_length=255,default="The Institute is dedicated to academic excellence and cutting-edge research, fostering a dynamic environment that encourages interdisciplinary learning, professional growth, and impactful innovation across various fields.")
    def __str__(self):
        return self.name


class Department(ImageResizeMixin,models.Model):
    id = models.AutoField(primary_key=True)  # Automatically generates a primary key
    name = models.CharField(max_length=255, unique=True)  # Unique name field
    image = models.ImageField(upload_to='images/department/', null=True,default='images/department/default.jpg')  
    description=models.TextField(max_length=255,default="The Department fosters innovative research and interdisciplinary collaboration, focusing on conceptual exploration and advanced academic problem-solving techniques.")
    institute = models.ForeignKey('Institute', related_name='departments', on_delete=models.CASCADE)  # Foreign key to Department
    def __str__(self):
        return self.name


class Course(ImageResizeMixin,models.Model):
    id = models.AutoField(primary_key=True)  # Automatically generates a primary key
    course_code = models.CharField(max_length=6, unique=True)  # Unique course code
    course_name = models.CharField(max_length=50)  # Course name
    course_description = models.TextField(
        default="This course provides a comprehensive overview of essential topics, methodologies, and concepts. Further details will be provided."
    )  # Description of the course
    department = models.ForeignKey('Department', related_name='courses', on_delete=models.CASCADE)  # Foreign key to Department
    
    image = models.ImageField(upload_to='images/course/', null=True, default='images/course/default.jpg')  # Course image

    def __str__(self):
        return self.course_name

    
class Faculty(ImageResizeMixin,models.Model):
    name = models.CharField(max_length=100)
    course = models.ForeignKey('Course', related_name='Faculty', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='images/faculty/', null=True,default='images/faculty/default.jpg')  
    position = models.CharField(max_length=100)
    
    # Add other relevant fields

    def __str__(self):
        return self.name

# Slide Model (Base)
class Slide(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey('Faculty', related_name='slides', on_delete=models.CASCADE, null=True, blank=True)
    content = models.FileField(upload_to=ContentUploadAdapter('slide').get_upload_strategy().get_upload_to)  # Adapter used for upload path
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Video Model (Base)
class Video(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey('Faculty', related_name='videos', on_delete=models.CASCADE, null=True, blank=True)
    content = models.FileField(upload_to=ContentUploadAdapter('video').get_upload_strategy().get_upload_to)  # Adapter used for upload path
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Note Model (Base)
class Note(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey('Faculty', related_name='notes', on_delete=models.CASCADE, null=True, blank=True)
    content = models.FileField(upload_to=ContentUploadAdapter('note').get_upload_strategy().get_upload_to)  # Adapter used for upload path
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Temporary Slide Model
class temp_Slide(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey('Faculty', related_name='temp_slides', on_delete=models.CASCADE, null=True, blank=True)
    real = models.ForeignKey(Slide, related_name='temp_versions', on_delete=models.CASCADE, null=True, blank=True)
    content = models.FileField(upload_to=ContentUploadAdapter('slide', is_temp=True).get_upload_strategy().get_upload_to)  # Adapter used for temporary upload path
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Temporary Video Model
class temp_Video(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey('Faculty', related_name='temp_videos', on_delete=models.CASCADE, null=True, blank=True)
    real = models.ForeignKey(Video, related_name='temp_versions', on_delete=models.CASCADE, null=True, blank=True)
    content = models.FileField(upload_to=ContentUploadAdapter('video', is_temp=True).get_upload_strategy().get_upload_to)  # Adapter used for temporary upload path
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Temporary Note Model
class temp_Note(models.Model):
    name = models.CharField(max_length=100)
    faculty = models.ForeignKey('Faculty', related_name='temp_notes', on_delete=models.CASCADE, null=True, blank=True)
    real = models.ForeignKey(Note, related_name='temp_versions', on_delete=models.CASCADE, null=True, blank=True)
    content = models.FileField(upload_to=ContentUploadAdapter('note', is_temp=True).get_upload_strategy().get_upload_to)  # Adapter used for temporary upload path
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name