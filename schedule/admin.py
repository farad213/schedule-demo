from django.contrib import admin
from .models import Vehicle, Project, Date, DateBoundWithProject, Profile, Artifact, Subproject


admin.site.register(Vehicle)
admin.site.register(Project)
admin.site.register(Date)
admin.site.register(DateBoundWithProject)

admin.site.register(Profile)
admin.site.register(Artifact)
admin.site.register(Subproject)
