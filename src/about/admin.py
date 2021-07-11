from django.contrib import admin
from django.db.models import QuerySet

from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    ordering = ['-created_at']
    list_display = ['created_at', 'text', 'user', 'read']
    list_filter = [
        ('read', admin.BooleanFieldListFilter),
    ]

    actions = ['make_not_read', 'make_read']

    @admin.action
    def make_not_read(self, request, queryset: QuerySet):
        queryset.update(read=False)

    @admin.action
    def make_read(self, request, queryset: QuerySet):
        queryset.update(read=True)
