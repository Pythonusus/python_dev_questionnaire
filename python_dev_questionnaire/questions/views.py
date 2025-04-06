from django.views.generic import DetailView
from django_filters.views import FilterView

from python_dev_questionnaire.questions.filters import QuestionFilter
from python_dev_questionnaire.questions.models import Question


class QuestionsIndexView(FilterView):
    model = Question
    context_object_name = 'questions'
    template_name = 'questions/questions_index.html'
    filterset_class = QuestionFilter


class QuestionDetailView(DetailView):
    """
    Display a single question.
    """
    model = Question
    context_object_name = 'question'
    template_name = 'questions/question_detail.html'
