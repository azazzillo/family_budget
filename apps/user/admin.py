# Django
from django.contrib import admin
# Local
from .models import (
    CustomUser, Family, FamilyUser
)


admin.site.register(CustomUser)
admin.site.register(Family)
admin.site.register(FamilyUser)
