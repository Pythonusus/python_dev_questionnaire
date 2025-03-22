from django.contrib import admin
from django.utils.text import Truncator

from python_dev_questionnaire.questions.models import Question, QuestionLabel


class QuestionLabelInline(admin.TabularInline):
    """
    Inline view for question labels in admin interface.
    Allows to create, add and edit labels while editing a question.
    """
    model = QuestionLabel
    extra = 1
    autocomplete_fields = ['label']
    verbose_name = "Метка"
    verbose_name_plural = "Метки"


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """Admin view for questions."""
    # Define truncation length as a class attribute
    truncation_length = 255

    list_display = [
        'truncated_question',
        'category',
        'truncated_answer',
        'get_labels',
        'created_at',
    ]
    fields = ['question', 'answer', 'category']
    inlines = [QuestionLabelInline]
    search_fields = ['question', 'answer', 'category__name']
    list_filter = ['category', 'labels', 'created_at']
    list_per_page = 10
    list_max_show_all = 20
    autocomplete_fields = ['category']

    def get_queryset(self, request):
        """Prefetch related labels for questions."""
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('labels')

    def truncated_question(self, obj):
        """Return truncated question text."""
        return Truncator(obj.question).chars(self.truncation_length)

    def truncated_answer(self, obj):
        """Return truncated answer text."""
        return Truncator(obj.answer).chars(self.truncation_length)

    def get_labels(self, obj):
        """Return a comma-separated list of labels for this question."""
        return ", ".join([label.name for label in obj.labels.all()])

    truncated_question.short_description = 'Вопрос'
    truncated_answer.short_description = 'Ответ'
    get_labels.short_description = 'Метки'
