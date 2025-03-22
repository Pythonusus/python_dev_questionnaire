from django.contrib import admin

from python_dev_questionnaire.labels.models import Label


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name', 'created_at']
    list_filter = ['created_at']
    list_per_page = 20
    list_max_show_all = 40
