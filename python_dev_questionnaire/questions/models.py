from django.db import models

from python_dev_questionnaire.categories.models import Category
from python_dev_questionnaire.labels.models import Label


class Question(models.Model):
    """
    A model to store a question, it'sanswer and it's metadata.
    """
    question = models.TextField(
        verbose_name='Вопрос',
        unique=True,
        blank=False,
        null=False,
    )
    answer = models.TextField(
        verbose_name='Ответ',
        unique=True,
        blank=False,
        null=False,
    )
    # Atleast one category must be created before creating a question
    # Does not allow deleting categories that are in use
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        verbose_name='Категория',
        related_name='questions',
        help_text='Категория к которой относится вопрос',
    )
    labels = models.ManyToManyField(
        Label,
        verbose_name='Метки',
        related_name='questions',
        help_text='Метки для данного вопроса',
        blank=True,
        through='QuestionLabel',
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата создания'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Дата обновления'
    )

    def __str__(self):
        return self.question

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class QuestionLabel(models.Model):
    """
    A model to store the relationship between a question and a label.
    Does not allow deleting labels that are in use.
    Default Django intermediate model is not enough for this case,
    because it allows to delete labels that are in use.
    """
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        verbose_name='Вопрос',
        related_name='question_labels',
    )

    label = models.ForeignKey(
        Label,
        on_delete=models.PROTECT,
        verbose_name='Метка',
        related_name='labels_questions',
    )

    def __str__(self):
        return f'{self.question.question} - {self.label.name}'
