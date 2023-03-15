from django.contrib import admin
from . models import BuildingsGMO, BuildingsGU, BuildingsGKB, BuildingsGEM, JelkodCCS, JelkodVVS, Technician, Customer

admin.site.register(BuildingsGMO)
admin.site.register(BuildingsGU)
admin.site.register(BuildingsGKB)
admin.site.register(BuildingsGEM)
admin.site.register(JelkodCCS)
admin.site.register(JelkodVVS)
admin.site.register(Technician)
admin.site.register(Customer)