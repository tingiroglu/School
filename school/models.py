from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with an extra type field"""
    USER_TYPE_CHOICES = (
        (1, 'manager'),
        (2, 'teacher'),
        (3, 'student'),
        (4, 'SuperUser'),
    )

    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)


class School(models.Model):
    """School object"""

    name = models.CharField(max_length=255)

    # manager = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # users = models.ManyToManyField(settings.AUTH_USER_MODEL)
    def __str__(self):
        return f"{self.name} "


class SchoolManager(models.Model):
    """Person object"""

    fullname = models.CharField(max_length=255)
    schl_manager = models.OneToOneField(
        School,
        on_delete=models.CASCADE
    )
    users = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fullname} - {str(self.schl_manager.name)}"


class Class(models.Model):
    """Class object"""

    name = models.CharField(max_length=255)
    # students = models.ManyToManyField(settings.AUTH_USER_MODEL)
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name} - {str(self.school.name)}"


class Teacher(models.Model):
    """School object"""
    name = models.CharField(max_length=255)
    class_obj = models.OneToOneField(Class, on_delete=models.CASCADE)
    school_ob = models.ForeignKey(School, on_delete=models.CASCADE, related_name='schools', blank=True)
    users = models.ForeignKey(settings.AUTH_USER_MODEL,  blank=True, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ("can_add_student", "Can add student"),
            ("can_change_student", "Can change student"),
            ("can_delete_student", "Can delete student"),
            ("can_view_student", "Can view student"),
        )

    def __str__(self):
        return f"{self.name} - {str(self.class_obj.name)}"


class Student(models.Model):
    """Person object"""

    fullname = models.CharField(max_length=255)
    classes = models.ForeignKey(
        Class,
        on_delete=models.CASCADE
    )
    schools = models.ForeignKey(
        School,
        on_delete=models.CASCADE
    )
    users = models.ForeignKey(settings.AUTH_USER_MODEL,  blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.fullname} - {str(self.classes.name)}"

    def __unicode__(self):
        return "studetn{0} - class{1}".format(Class.pk, School.pk)
