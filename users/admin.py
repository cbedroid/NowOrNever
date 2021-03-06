from django.contrib import admin
from .models import Profile, NewsLetter


class DateCreateAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created",
        "updated",
    )

admin.site.register(Profile, DateCreateAdmin)
admin.site.register(NewsLetter, DateCreateAdmin)
