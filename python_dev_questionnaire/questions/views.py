from django.views.generic import DetailView, ListView

from python_dev_questionnaire.questions.models import Question


class QuestionsIndexView(ListView):
    model = Question
    context_object_name = 'questions'
    template_name = 'questions/questions_index.html'


class QuestionDetailView(DetailView):
    """
    Display a single question.
    """
    model = Question
    context_object_name = 'question'
    template_name = 'questions/question_detail.html'
