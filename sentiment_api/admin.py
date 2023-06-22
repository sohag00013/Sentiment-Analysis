from django.contrib import admin

# Register your models here.
from .models import Positive, Negative, Neutral
admin.site.register(Positive)
admin.site.register(Negative)
admin.site.register(Neutral)


