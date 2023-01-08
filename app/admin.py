from django.contrib import admin
from .models import PayrollAccount, Employee, PayStatement

admin.site.register([PayrollAccount, Employee, PayStatement])
