from django.contrib import admin

# Register your models here.
from .models import Values
from .models import Datapoint

admin.site.register(Values)
admin.site.register(Datapoint)