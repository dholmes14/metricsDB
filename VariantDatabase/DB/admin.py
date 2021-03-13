from django.contrib import admin
from .models import Patient_data, Variant_data, Test_data, Interpretation_data

admin.site.register(Patient_data)
admin.site.register(Variant_data)
admin.site.register(Test_data)
admin.site.register(Interpretation_data)
