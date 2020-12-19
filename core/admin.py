from django.contrib import admin
from django.utils.html import mark_safe
from .models import ContactUs, Rating


class DateCreateAdmin(admin.ModelAdmin):
    readonly_fields = (
        "created",
        "updated",
    )


class ContactUsReadOnly(admin.ModelAdmin):
    readonly_fields = [x.name for x in ContactUs._meta.fields]

    def makeCheckBox(self, obj):
        is_checked = "checked" if obj.has_account else ""
        return mark_safe(
        f'<input disabled type="checkbox" class="admin_checkbox" name="account" value="has_account" {is_checked}>'
        )

    makeCheckBox.short_description = "has Account"
    list_display = [
        "firstname", "lastname", "makeCheckBox",
    ]


admin.site.register(Rating, DateCreateAdmin)
admin.site.register(ContactUs, ContactUsReadOnly)
