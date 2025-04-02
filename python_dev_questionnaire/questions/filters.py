from django_filters import (
    DateRangeFilter,
    FilterSet,
    ModelChoiceFilter,
    OrderingFilter,
)

from python_dev_questionnaire.categories.models import Category
from python_dev_questionnaire.labels.models import Label
from python_dev_questionnaire.questions.models import Question


class QuestionFilter(FilterSet):
    category = ModelChoiceFilter(
        queryset=Category.objects.all(),
        label='Категория',
        empty_label='Все категории',
    )
    label1 = ModelChoiceFilter(
        queryset=Label.objects.all(),
        label='Метка 1',
        method='filter_labels',
    )
    label2 = ModelChoiceFilter(
        queryset=Label.objects.all(),
        label='Метка 2',
        method='filter_labels',
        required=False,
    )
    created_at = DateRangeFilter(
        label='Дата создания',
        empty_label='Любая',
        choices=[
            ('today', 'Сегодня'),
            ('yesterday', 'Вчера'),
            ('week', 'За 7 дней'),
            ('month', 'За месяц'),
            ('year', 'За год'),
        ],
    )

    order_by = OrderingFilter(
        label='Сортировка',
        choices=(
            ('-created_at', 'Сначала новые'),
            ('created_at', 'Сначала старые'),
        ),
    )

    def filter_labels(self, queryset, name, value):
        """
        Custom filter method to handle multiple label filtering.
        Each selected label is added to the filter with AND logic.
        """
        if value:
            return queryset.filter(labels=value)
        return queryset

    class Meta:
        model = Question
        fields = [
            'category',
            'label1',
            'label2',
            'created_at',
            'order_by',
        ]
        order_by_field = 'order_by'
        order_by = ['-created_at']
