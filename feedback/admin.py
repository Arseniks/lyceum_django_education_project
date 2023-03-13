from django.contrib import admin

import feedback.models


class FeedbackTextInline(admin.TabularInline):
    model = feedback.models.FeedbackText
    readonly_fields = ('text',)


class FeedbackFilesInline(admin.TabularInline):
    model = feedback.models.FeedbackFiles
    readonly_fields = ('files',)


@admin.register(feedback.models.Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        feedback.models.Feedback.mail.field.name,
        feedback.models.Feedback.status.field.name,
    )
    inlines = [
        FeedbackTextInline,
        FeedbackFilesInline,
    ]
