from django.contrib import admin
from .models import ContactUs

# Register your models here.


class DateCreateAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created",
        "updated",
    )


admin.site.register(ContactUs, DateCreateAdmin)
