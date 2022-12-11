from django.contrib import admin
from . models import BuildingsTMO, BuildingsTU, BuildingsTKB, BuildingsTEM

admin.site.register(BuildingsTMO)
admin.site.register(BuildingsTU)
admin.site.register(BuildingsTKB)
admin.site.register(BuildingsTEM)
