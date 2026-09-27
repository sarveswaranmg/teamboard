from django.contrib import admin
from .models import Company, KBEntry, QueryLog


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "company_name",
        "user",
        "role",
        "api_key",
        "created_at",
    )


@admin.register(KBEntry)
class KBEntryAdmin(admin.ModelAdmin):
    list_display = (
        "question",
        "category",
        "created_at",
    )


@admin.register(QueryLog)
class QueryLogAdmin(admin.ModelAdmin):
    list_display = (
        "company",
        "search_term",
        "results_count",
        "queried_at",
    )