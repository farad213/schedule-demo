from django.db import models
from django.contrib.auth.models import User
from functools import partial


class Vehicle(models.Model):
    license_plate = models.CharField(max_length=20, verbose_name="Rendszám")
    vehicle_name = models.CharField(max_length=30, verbose_name="Autó neve")

    class Meta:
        verbose_name = "Jármű"
        verbose_name_plural = "Járművek"

    def __str__(self):
        return self.vehicle_name


class Project(models.Model):
    project = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Munkatípus"
        verbose_name_plural = "Munkatípusok"

    def hasSubproject(self):
        return self.subproject.exists()

    def __str__(self):
        return self.project




class Subproject(models.Model):
    subproject = models.CharField(max_length=50, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, related_name="subproject")
    name = models.CharField(max_length=100, null=True)
    customer = models.CharField(max_length=100, null=True)

    class Meta:
        verbose_name = "Süllyedésmérés iktatószám"
        verbose_name_plural = "Süllyedésmérés iktatószámok"

    def __str__(self):
        return self.subproject


class Artifact(models.Model):
    subproject = models.ForeignKey(Subproject, on_delete=models.CASCADE)
    artifact = models.CharField(max_length=50, verbose_name="Műtárgy", null=True)

    class Meta:
        verbose_name = "Műtárgy"
        verbose_name_plural = "Műtárgyak"

    def __str__(self):
        return self.artifact


class Profile(models.Model):
    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE, verbose_name="Műtárgy")
    profile = models.CharField(max_length=50, verbose_name="Szelvény", null=True)
    length = models.IntegerField(null=True, blank=True, verbose_name="Csőhossz")
    measurement_side = models.CharField(max_length=10, null=True, blank=True, verbose_name="Mérési oldal")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Földrajzi hosszúság")
    latitude = models.FloatField(null=True, blank=True, verbose_name="Földrajzi szélesség")

    class Meta:
        verbose_name = "Süllyedésmérő cső"
        verbose_name_plural = "Süllyedésmérő csövek"

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

    class Meta:
        verbose_name = "Dátum"
        verbose_name_plural = "Dátumok"


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

class SIT_project(models.Model):
    project_no = models.CharField(max_length=30)
    customer = models.CharField(max_length=50)
    contract = models.IntegerField()
    location = models.CharField(max_length=100)

    class Meta:
        verbose_name = "SIT iktatószám"
        verbose_name_plural = "SIT iktatószámok"

    def __str__(self):
        return self.project_no


class SIT_with_date(models.Model):
    date_bound_with_project_object = models.ForeignKey(DateBoundWithProject, on_delete=models.CASCADE)
    project_no = models.ForeignKey(SIT_project, on_delete=models.CASCADE, verbose_name="Iktatószám")
    bridge = models.CharField(max_length=100, verbose_name="Híd jele")
    building = models.CharField(max_length=100, verbose_name="Épület/Támasz")
    no_of_piles = models.IntegerField(verbose_name="Cölöpök száma")

    class Meta:
        verbose_name = "Rögzített SIT projekt"
        verbose_name_plural = "Rögzített SIT projektek"

    def __str__(self):
        return f"{self.project_no} - {self.date_bound_with_project_object.date.date}"
