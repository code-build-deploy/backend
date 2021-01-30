from django.contrib import admin
from .models import Param, User, Certificate, Organisation
# Register your models here.
admin.site.register(Param)
admin.site.register(User)
admin.site.register(Certificate)
admin.site.register(Organisation)