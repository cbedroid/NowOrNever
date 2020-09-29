from django.contrib import admin
from .models import ContactUs, Rating


class DateCreateAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created",
        "updated",
    )


admin.site.register(ContactUs, DateCreateAdmin)
admin.site.register(Rating, DateCreateAdmin)
