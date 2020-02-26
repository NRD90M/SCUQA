from django.contrib import admin

# Register your models here.
from QA import models

admin.site.register(models.User)
#admin.site.register(models.Suggestion)
admin.site.register(models.EmailVerifyRecord)