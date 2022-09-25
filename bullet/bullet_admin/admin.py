from bullet_admin.models import BranchRole, CompetitionRole
from django.contrib import admin


@admin.register(BranchRole)
class BranchRoleAdmin(admin.ModelAdmin):
    list_display = ("branch", "user", "is_translator", "is_admin")
    list_filter = ("branch",)
    autocomplete_fields = ("user",)


@admin.register(CompetitionRole)
class CompetitionRoleAdmin(admin.ModelAdmin):
    list_display = ("competition", "user", "country", "venue")
    list_filter = ("competition",)
    autocomplete_fields = ("user", "venue")
