from django.contrib import admin
from . models import BuildingsTMO, BuildingsTU, BuildingsTKB, BuildingsTEM, JelkodCCS, JelkodVVS, Technician, Customer

admin.site.register(BuildingsTMO)
admin.site.register(BuildingsTU)
admin.site.register(BuildingsTKB)
admin.site.register(BuildingsTEM)
admin.site.register(JelkodCCS)
admin.site.register(JelkodVVS)
admin.site.register(Technician)
admin.site.register(Customer)