from django.db import models


class Employee(models.Model):
    employee_name = models.CharField(max_length=50)
    nickname = models.CharField(max_length=30)

    def __str__(self):
        return self.nickname


class Vehicle(models.Model):
    license_plate = models.CharField(max_length=20)
    vehicle_name = models.CharField(max_length=30)

    def __str__(self):
        return self.vehicle_name

class SubProjectName(models.Model):
    subproject = models.CharField(max_length=100)


class SubProjectItem(models.Model):
    sub_project_item = models.CharField(max_length=50)
    sub_project_name = models.ForeignKey(SubProjectName, on_delete=models.CASCADE)


class Project(models.Model):
    project = models.CharField(max_length=50)
    subproject = models.ForeignKey

    def __str__(self):
        return self.project


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

    def __str__(self):
        return f'{self.date} {self.project}'
