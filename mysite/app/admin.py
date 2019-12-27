from django.contrib import admin
from .models import Params, User, Certificate
# Register your models here.
admin.site.register(Params)
admin.site.register(User)
admin.site.register(Certificate)