from django.contrib import admin
from .models import Profile

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "main_lin",
        "sublin",
        "drtype",
        "num_dr_variants",
        "num_other_variants"
    )

admin.site.register(Profile, ProfileAdmin)