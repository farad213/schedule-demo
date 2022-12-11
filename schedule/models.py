from django.db import models


class Employee(models.Model):
    employee_name = models.CharField(max_length=50, verbose_name="Munkavállaló neve")
    nickname = models.CharField(max_length=30, verbose_name="Munkavállaló beceneve")

    def __str__(self):
        return self.nickname


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

    def __str__(self):
        return self.subproject


class Artifact(models.Model):
    subproject = models.ForeignKey(Subproject, on_delete=models.CASCADE)
    artifact = models.CharField(max_length=50, verbose_name="Műtárgy", null=True)

    def __str__(self):
        return self.artifact


class Profile(models.Model):
    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE)
    profile = models.CharField(max_length=50, verbose_name="Szelvény", null=True, blank=True)

    def __str__(self):
        return self.profile


class Date(models.Model):
    date = models.DateField(null=True)

    def __str__(self):
        return self.date.strftime("%Y.%m.%d")

class DateBoundWithProject(models.Model):
    date = models.ForeignKey(Date, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    employee = models.ManyToManyField(Employee)
    vehicle = models.ManyToManyField(Vehicle)
    comment = models.TextField(null=True, blank=True)
    subproject = models.ForeignKey(Subproject, on_delete=models.CASCADE, null=True)
    artifact = models.ForeignKey(Artifact, on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.date} {self.project}'
