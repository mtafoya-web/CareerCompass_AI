from django.contrib import admin
from .models import Recommendation, ActionPlanItem
# Register your models here.
admin.site.register(Recommendation, ActionPlanItem)