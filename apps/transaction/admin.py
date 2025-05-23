# Django
from django.contrib import admin
# Local
from transaction.models import(
    Category, Transaction
)


admin.site.register(Category)
admin.site.register(Transaction)
