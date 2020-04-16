from django.contrib import admin

from main import models

admin.site.register(models.main.ImportedHospital)
admin.site.register(models.main.Hospital)
admin.site.register(models.main.AidRequest)
admin.site.register(models.user.User)
