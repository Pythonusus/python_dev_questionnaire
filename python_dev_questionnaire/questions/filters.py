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
    """
    Filter class for filtering questions based on category, labels, and date.
    """
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
        Custom filter method to handle multiple label filtering with AND logic.

        Args:
            queryset (QuerySet): The initial queryset to filter
            name (str): The name of the filter field that called this method
            value (Label): The Label instance selected in the filter

        Returns:
            QuerySet: A filtered queryset
        """
        if value:
            # Get all selected label values
            filters = set()
            for filter_name in ['label1', 'label2']:
                filter_value = self.data.get(filter_name)
                if filter_value:
                    filters.add(filter_value)

            # Apply all label filters with AND logic
            filtered_queryset = queryset
            for label_value in filters:
                filtered_queryset = filtered_queryset.filter(
                    labels=label_value
                )
            return filtered_queryset
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
        # Default ordering
        order_by_field = 'order_by'
        order_by = ['-created_at']
