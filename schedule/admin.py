from django.contrib import admin
from .models import Employee, Vehicle, Project, Date, DateBoundWithProject


admin.site.register(Employee)
admin.site.register(Vehicle)
admin.site.register(Project)
admin.site.register(Date)
admin.site.register(DateBoundWithProject)
