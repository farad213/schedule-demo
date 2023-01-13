from django.db import models
from django.contrib.auth.models import User
from functools import partial


class Vehicle(models.Model):
    license_plate = models.CharField(max_length=20, verbose_name="Rendszám")
    vehicle_name = models.CharField(max_length=30, verbose_name="Autó neve")

    def __str__(self):
        return self.vehicle_name


class Project(models.Model):
    project = models.CharField(max_length=50)

    def hasSubproject(self):
        return self.subproject.exists()

    def __str__(self):
        return self.project


class Subproject(models.Model):
    subproject = models.CharField(max_length=50, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, related_name="subproject")
    name = models.CharField(max_length=100, null=True)
    customer = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.subproject


class Artifact(models.Model):
    subproject = models.ForeignKey(Subproject, on_delete=models.CASCADE)
    artifact = models.CharField(max_length=50, verbose_name="Műtárgy", null=True)

    def __str__(self):
        return self.artifact


class Profile(models.Model):
    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE)
    profile = models.CharField(max_length=50, verbose_name="Szelvény", null=True)
    length = models.IntegerField(null=True)
    measurement_side = models.CharField(max_length=10, null=True)
    longitude = models.FloatField(null=True)
    latitude = models.FloatField(null=True)

    def __str__(self):
        return self.profile


class Date(models.Model):
    date = models.DateField(null=True)
    state = models.CharField(max_length=15, choices=[("untouched", "untouched"), ("draft", "draft"), ("done", "done")],
                             default="untouched")
    employees_on_leave = models.ManyToManyField(User, blank=True)

    def hasProjectFunc(self, project):
        if DateBoundWithProject.objects.filter(date=self, project=project):
            return "true"
        else:
            return "false"

    def hasProject(self):
        self.hasProject = {f"{project.__str__()}": partial(self.hasProjectFunc, project=project) for project in
                      Project.objects.all()}
        return self.hasProject

    def __str__(self):
        return self.date.strftime("%Y.%m.%d")


class DateBoundWithProject(models.Model):
    date = models.ForeignKey(Date, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    employee = models.ManyToManyField(User)
    vehicle = models.ManyToManyField(Vehicle)
    comment = models.TextField(null=True, blank=True)
    subproject = models.ForeignKey(Subproject, on_delete=models.CASCADE, null=True)
    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE, null=True)
    profile = models.ManyToManyField(Profile, blank=True)

    def __str__(self):
        return f'{self.date} {self.project}'
